from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select,desc
from app.db.session import get_db
from app.core.security import get_current_user
from app.models import DeletionHistory
router=APIRouter(prefix='/history',tags=['History'])
@router.get('/deletions')
def deletions(db:Session=Depends(get_db),u=Depends(get_current_user)):
    return [dict(id=x.id,file_id=x.file_id,original_name=x.original_name,size_bytes=x.size_bytes,reason=x.reason,deleted_at=x.deleted_at) for x in db.scalars(select(DeletionHistory).where(DeletionHistory.user_id==u.id).order_by(desc(DeletionHistory.deleted_at))).all()]
