from app.db.session import SessionLocal
from app.models import User
from app.core.security import hash_password
from sqlalchemy import select
with SessionLocal() as db:
    if not db.scalar(select(User).where(User.email=='admin@example.com')):
        db.add(User(name='Admin User',email='admin@example.com',password_hash=hash_password('Admin@123'))); db.commit()
print('Demo user: admin@example.com / Admin@123')
