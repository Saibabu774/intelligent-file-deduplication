from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base,engine
import app.models
from app.api import auth,files,duplicates,dashboard,history
Path(settings.storage_dir).mkdir(parents=True,exist_ok=True)
app=FastAPI(title=settings.app_name,version='1.0.0',description='Secure file management, duplicate detection and storage optimization API')
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_list,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(auth.router,prefix='/api/v1'); app.include_router(files.router,prefix='/api/v1'); app.include_router(duplicates.router,prefix='/api/v1'); app.include_router(dashboard.router,prefix='/api/v1'); app.include_router(history.router,prefix='/api/v1')
@app.on_event('startup')
def startup(): Base.metadata.create_all(bind=engine)
@app.get('/')
def root(): return {'message':'Intelligent File Deduplication API','docs':'/docs','version':'1.0.0'}
