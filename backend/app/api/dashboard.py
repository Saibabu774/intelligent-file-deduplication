from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select,func,desc
from app.db.session import get_db
from app.core.security import get_current_user
from app.models import File,FileHash,DuplicateGroup
from app.schemas.file import DashboardOut,FileOut
router=APIRouter(prefix='/dashboard',tags=['Dashboard'])
def dto(f): return FileOut(id=f.id,original_name=f.original_name,mime_type=f.mime_type,extension=f.extension,size_bytes=f.size_bytes,status=f.status,is_protected=f.is_protected,created_at=f.created_at,hash_value=f.hash_record.hash_value if f.hash_record else None)
@router.get('',response_model=DashboardOut)
def dashboard(db:Session=Depends(get_db),u=Depends(get_current_user)):
    base=select(File).where(File.user_id==u.id,File.status!='deleted'); fs=list(db.scalars(base).all()); dup_hashes={h for h,n in db.execute(select(FileHash.hash_value,func.count(FileHash.id)).group_by(FileHash.hash_value).having(func.count(FileHash.id)>1)).all()}
    dup=[f for f in fs if f.hash_record and f.hash_record.hash_value in dup_hashes]
    savings=sum(g.potential_savings for g in db.scalars(select(DuplicateGroup)).all())
    return DashboardOut(total_files=len(fs),total_storage=sum(f.size_bytes for f in fs),duplicate_files=len(dup),duplicate_storage=sum(f.size_bytes for f in dup),potential_savings=savings,largest_files=[dto(f) for f in sorted(fs,key=lambda x:x.size_bytes,reverse=True)[:5]],recent_uploads=[dto(f) for f in sorted(fs,key=lambda x:x.created_at,reverse=True)[:5]])
