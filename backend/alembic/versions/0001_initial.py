"""initial schema"""
from alembic import op
import sqlalchemy as sa
revision='0001_initial'; down_revision=None; branch_labels=None; depends_on=None
def upgrade():
 op.create_table('users',sa.Column('id',sa.Integer,primary_key=True),sa.Column('name',sa.String(120),nullable=False),sa.Column('email',sa.String(255),unique=True,index=True),sa.Column('password_hash',sa.String(255),nullable=False),sa.Column('is_active',sa.Boolean,default=True),sa.Column('created_at',sa.DateTime))
 op.create_table('files',sa.Column('id',sa.Integer,primary_key=True),sa.Column('user_id',sa.Integer,sa.ForeignKey('users.id'),index=True),sa.Column('original_name',sa.String(255),index=True),sa.Column('stored_name',sa.String(255),unique=True),sa.Column('storage_path',sa.String(1024)),sa.Column('mime_type',sa.String(150)),sa.Column('extension',sa.String(20),index=True),sa.Column('size_bytes',sa.BigInteger,index=True),sa.Column('status',sa.String(30),index=True),sa.Column('is_protected',sa.Boolean),sa.Column('created_at',sa.DateTime,index=True),sa.Column('deleted_at',sa.DateTime))
 op.create_table('file_hashes',sa.Column('id',sa.Integer,primary_key=True),sa.Column('file_id',sa.Integer,sa.ForeignKey('files.id',ondelete='CASCADE'),unique=True,index=True),sa.Column('algorithm',sa.String(30)),sa.Column('hash_value',sa.String(128),index=True),sa.Column('created_at',sa.DateTime))
 op.create_table('file_metadata',sa.Column('id',sa.Integer,primary_key=True),sa.Column('file_id',sa.Integer,sa.ForeignKey('files.id',ondelete='CASCADE'),unique=True),sa.Column('width',sa.Integer),sa.Column('height',sa.Integer),sa.Column('metadata_json',sa.Text))
 op.create_table('duplicate_groups',sa.Column('id',sa.Integer,primary_key=True),sa.Column('hash_value',sa.String(128),unique=True,index=True),sa.Column('original_file_id',sa.Integer,sa.ForeignKey('files.id')),sa.Column('file_count',sa.Integer),sa.Column('total_size',sa.BigInteger),sa.Column('potential_savings',sa.BigInteger),sa.Column('created_at',sa.DateTime))
 op.create_table('deletion_history',sa.Column('id',sa.Integer,primary_key=True),sa.Column('file_id',sa.Integer,index=True),sa.Column('user_id',sa.Integer,sa.ForeignKey('users.id')),sa.Column('original_name',sa.String(255)),sa.Column('size_bytes',sa.BigInteger),sa.Column('reason',sa.String(255)),sa.Column('deleted_at',sa.DateTime))
 op.create_table('audit_logs',sa.Column('id',sa.Integer,primary_key=True),sa.Column('user_id',sa.Integer,sa.ForeignKey('users.id')),sa.Column('action',sa.String(100),index=True),sa.Column('entity_type',sa.String(50)),sa.Column('entity_id',sa.Integer),sa.Column('details',sa.Text),sa.Column('created_at',sa.DateTime))
def downgrade():
 for t in ['audit_logs','deletion_history','duplicate_groups','file_metadata','file_hashes','files','users']: op.drop_table(t)
