from sqlalchemy import String, BigInteger, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.db.session import Base
class File(Base):
    __tablename__='files'
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey('users.id'),index=True)
    original_name:Mapped[str]=mapped_column(String(255),index=True)
    stored_name:Mapped[str]=mapped_column(String(255),unique=True)
    storage_path:Mapped[str]=mapped_column(String(1024))
    mime_type:Mapped[str|None]=mapped_column(String(150),nullable=True)
    extension:Mapped[str|None]=mapped_column(String(20),nullable=True,index=True)
    size_bytes:Mapped[int]=mapped_column(BigInteger,index=True)
    status:Mapped[str]=mapped_column(String(30),default='processing',index=True)
    is_protected:Mapped[bool]=mapped_column(Boolean,default=False)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc),index=True)
    deleted_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
    owner=relationship('User',back_populates='files')
    hash_record=relationship('FileHash',back_populates='file',uselist=False,cascade='all, delete-orphan')
    metadata_record=relationship('FileMetadata',back_populates='file',uselist=False,cascade='all, delete-orphan')
class FileHash(Base):
    __tablename__='file_hashes'
    id:Mapped[int]=mapped_column(primary_key=True)
    file_id:Mapped[int]=mapped_column(ForeignKey('files.id',ondelete='CASCADE'),unique=True,index=True)
    algorithm:Mapped[str]=mapped_column(String(30),default='sha256')
    hash_value:Mapped[str]=mapped_column(String(128),index=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
    file=relationship('File',back_populates='hash_record')
class FileMetadata(Base):
    __tablename__='file_metadata'
    id:Mapped[int]=mapped_column(primary_key=True)
    file_id:Mapped[int]=mapped_column(ForeignKey('files.id',ondelete='CASCADE'),unique=True)
    width:Mapped[int|None]=mapped_column(Integer,nullable=True)
    height:Mapped[int|None]=mapped_column(Integer,nullable=True)
    metadata_json:Mapped[str|None]=mapped_column(Text,nullable=True)
    file=relationship('File',back_populates='metadata_record')
class DuplicateGroup(Base):
    __tablename__='duplicate_groups'
    id:Mapped[int]=mapped_column(primary_key=True)
    hash_value:Mapped[str]=mapped_column(String(128),unique=True,index=True)
    original_file_id:Mapped[int|None]=mapped_column(ForeignKey('files.id'),nullable=True)
    file_count:Mapped[int]=mapped_column(Integer,default=0)
    total_size:Mapped[int]=mapped_column(BigInteger,default=0)
    potential_savings:Mapped[int]=mapped_column(BigInteger,default=0)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
class DeletionHistory(Base):
    __tablename__='deletion_history'
    id:Mapped[int]=mapped_column(primary_key=True)
    file_id:Mapped[int]=mapped_column(Integer,index=True)
    user_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
    original_name:Mapped[str]=mapped_column(String(255))
    size_bytes:Mapped[int]=mapped_column(BigInteger)
    reason:Mapped[str]=mapped_column(String(255),default='duplicate cleanup')
    deleted_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
class AuditLog(Base):
    __tablename__='audit_logs'
    id:Mapped[int]=mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
    action:Mapped[str]=mapped_column(String(100),index=True)
    entity_type:Mapped[str]=mapped_column(String(50))
    entity_id:Mapped[int|None]=mapped_column(Integer,nullable=True)
    details:Mapped[str|None]=mapped_column(Text,nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
