from app.tasks.celery_app import celery
from app.db.session import SessionLocal
from app.models import File, FileHash
from app.services.hashing import sha256_file
from app.services.duplicates import rebuild_group
@celery.task(name='hash_file_task')
def hash_file_task(file_id:int):
    db=SessionLocal(); f=db.get(File,file_id)
    if not f: db.close(); return
    try:
        hv=sha256_file(__import__('pathlib').Path(f.storage_path))
        existing=db.scalar(__import__('sqlalchemy').select(FileHash).where(FileHash.file_id==file_id))
        if not existing: db.add(FileHash(file_id=file_id,hash_value=hv))
        else: existing.hash_value=hv
        f.status='ready'; db.commit(); rebuild_group(db,hv); db.commit()
    except Exception: f.status='failed'; db.commit(); raise
    finally: db.close()
