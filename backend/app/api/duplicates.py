from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.core.security import get_current_user
from app.models import DuplicateGroup, File, FileHash
from app.schemas.file import DuplicateGroupOut, DuplicateItem
router=APIRouter(prefix='/duplicates',tags=['Duplicates'])
@router.get('/groups',response_model=list[DuplicateGroupOut])
def groups(db:Session=Depends(get_db),u=Depends(get_current_user)):
    out=[]
    for g in db.scalars(select(DuplicateGroup).order_by(DuplicateGroup.potential_savings.desc())).all():
        fs=db.scalars(select(File).join(FileHash).where(FileHash.hash_value==g.hash_value,File.user_id==u.id,File.status!='deleted').order_by(File.created_at)).all()
        if len(fs)>=2: out.append(DuplicateGroupOut(id=g.id,hash_value=g.hash_value,file_count=len(fs),total_size=sum(x.size_bytes for x in fs),potential_savings=sum(x.size_bytes for x in fs[1:]),files=[DuplicateItem(id=x.id,original_name=x.original_name,size_bytes=x.size_bytes,created_at=x.created_at,is_protected=x.is_protected) for x in fs]))
    return out
