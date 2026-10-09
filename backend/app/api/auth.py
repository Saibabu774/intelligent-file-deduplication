from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.models import User
from app.schemas.auth import RegisterRequest, LoginRequest, UserOut
from app.schemas.common import Token
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
router=APIRouter(prefix='/auth',tags=['Authentication'])
@router.post('/register',response_model=UserOut)
def register(data:RegisterRequest,db:Session=Depends(get_db)):
    if db.scalar(select(User).where(User.email==data.email)): raise HTTPException(409,'Email already registered')
    u=User(name=data.name,email=data.email,password_hash=hash_password(data.password)); db.add(u); db.commit(); db.refresh(u); return u
@router.post('/login',response_model=Token)
def login(data:LoginRequest,db:Session=Depends(get_db)):
    u=db.scalar(select(User).where(User.email==data.email))
    if not u or not verify_password(data.password,u.password_hash): raise HTTPException(401,'Incorrect email or password')
    return {'access_token':create_access_token({'sub':str(u.id)}),'token_type':'bearer'}
@router.get('/me',response_model=UserOut)
def me(u=Depends(get_current_user)): return u
