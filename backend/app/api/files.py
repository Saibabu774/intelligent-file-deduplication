from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, UploadFile, File as UploadFileType, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, desc
from app.db.session import get_db
from app.core.config import settings
from app.core.security import get_current_user
from app.models import File, FileHash, DeletionHistory, AuditLog
from app.schemas.file import FileOut
from app.schemas.common import Message
from app.tasks.hash_tasks import hash_file_task
router=APIRouter(prefix='/files',tags=['Files'])

def dto(f): return FileOut(id=f.id,original_name=f.original_name,mime_type=f.mime_type,extension=f.extension,size_bytes=f.size_bytes,status=f.status,is_protected=f.is_protected,created_at=f.created_at,hash_value=f.hash_record.hash_value if f.hash_record else None)
@router.post('/upload',response_model=FileOut)
async def upload(file:UploadFile=UploadFileType(...),db:Session=Depends(get_db),u=Depends(get_current_user)):
    ext=Path(file.filename or '').suffix.lower().lstrip('.')
    if ext not in settings.allowed_ext_set: raise HTTPException(415,'File type is not allowed')
    user_dir=Path(settings.storage_dir)/str(u.id); user_dir.mkdir(parents=True,exist_ok=True)
    stored=f'{uuid4().hex}{Path(file.filename).suffix.lower()}'; path=user_dir/stored; total=0
    with path.open('wb') as out:
        while chunk:=await file.read(1024*1024):
            total+=len(chunk)
            if total>settings.max_upload_size_mb*1024*1024: path.unlink(missing_ok=True); raise HTTPException(413,'File too large')
            out.write(chunk)
    f=File(user_id=u.id,original_name=file.filename or stored,stored_name=stored,storage_path=str(path),mime_type=file.content_type,extension=ext,size_bytes=total)
    db.add(f); db.commit(); db.refresh(f); db.add(AuditLog(user_id=u.id,action='UPLOAD',entity_type='file',entity_id=f.id,details=f.original_name)); db.commit(); hash_file_task.delay(f.id); return dto(f)
@router.get('',response_model=list[FileOut])
def list_files(search:str|None=None,extension:str|None=None,duplicate_only:bool=False,min_size:int|None=None,max_size:int|None=None,skip:int=0,limit:int=25,sort_by:str='created_at',sort_order:str='desc',db:Session=Depends(get_db),u=Depends(get_current_user)):
    q=select(File).where(File.user_id==u.id,File.status!='deleted')
    if search: q=q.where(File.original_name.like(f'%{search}%'))
    if extension: q=q.where(File.extension==extension.lower().lstrip('.'))
    if min_size is not None: q=q.where(File.size_bytes>=min_size)
    if max_size is not None: q=q.where(File.size_bytes<=max_size)
    if duplicate_only: q=q.join(FileHash).group_by(File.id).having(func.count(FileHash.id)>0).where(FileHash.hash_value.in_(select(FileHash.hash_value).group_by(FileHash.hash_value).having(func.count(FileHash.id)>1)))
    col=getattr(File,sort_by,File.created_at); q=q.order_by(desc(col) if sort_order=='desc' else col).offset(skip).limit(min(limit,100)); return [dto(f) for f in db.scalars(q).all()]
@router.get('/{file_id}',response_model=FileOut)
def get_file(file_id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
    f=db.scalar(select(File).where(File.id==file_id,File.user_id==u.id,File.status!='deleted'))
    if not f: raise HTTPException(404,'File not found')
    return dto(f)
@router.get('/{file_id}/download')
def download(file_id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
    f=db.scalar(select(File).where(File.id==file_id,File.user_id==u.id,File.status!='deleted'))
    if not f or not Path(f.storage_path).exists(): raise HTTPException(404,'File not found')
    return FileResponse(f.storage_path,filename=f.original_name,media_type=f.mime_type or 'application/octet-stream')
@router.delete('/{file_id}',response_model=Message)
def delete_file(file_id:int,db:Session=Depends(get_db),u=Depends(get_current_user)):
    f=db.scalar(select(File).where(File.id==file_id,File.user_id==u.id,File.status!='deleted'))
    if not f: raise HTTPException(404,'File not found')
    if f.is_protected: raise HTTPException(403,'Protected files cannot be deleted')
    f.status='deleted'; f.deleted_at=__import__('datetime').datetime.utcnow(); db.add(DeletionHistory(file_id=f.id,user_id=u.id,original_name=f.original_name,size_bytes=f.size_bytes)); db.add(AuditLog(user_id=u.id,action='DELETE',entity_type='file',entity_id=f.id,details=f.original_name)); db.commit(); Path(f.storage_path).unlink(missing_ok=True); return {'message':'File deleted safely'}
