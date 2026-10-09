from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models import File, FileHash, DuplicateGroup
def rebuild_group(db:Session, hash_value:str):
    files=list(db.scalars(select(File).join(FileHash).where(FileHash.hash_value==hash_value, File.status!='deleted').order_by(File.created_at,File.id)))
    group=db.scalar(select(DuplicateGroup).where(DuplicateGroup.hash_value==hash_value))
    if len(files)<2:
        if group: db.delete(group)
        return
    if not group: group=DuplicateGroup(hash_value=hash_value); db.add(group)
    group.original_file_id=files[0].id; group.file_count=len(files); group.total_size=sum(f.size_bytes for f in files); group.potential_savings=sum(f.size_bytes for f in files[1:])
