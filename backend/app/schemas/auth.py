from pydantic import BaseModel, EmailStr, ConfigDict
class RegisterRequest(BaseModel): name:str; email:EmailStr; password:str
class LoginRequest(BaseModel): email:EmailStr; password:str
class UserOut(BaseModel): model_config=ConfigDict(from_attributes=True); id:int; name:str; email:EmailStr
