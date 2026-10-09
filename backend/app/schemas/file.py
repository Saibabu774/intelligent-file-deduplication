from pydantic import BaseModel, ConfigDict
from datetime import datetime
class FileOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; original_name:str; mime_type:str|None; extension:str|None; size_bytes:int; status:str; is_protected:bool; created_at:datetime; hash_value:str|None=None
class DuplicateItem(BaseModel): id:int; original_name:str; size_bytes:int; created_at:datetime; is_protected:bool
class DuplicateGroupOut(BaseModel): id:int; hash_value:str; file_count:int; total_size:int; potential_savings:int; files:list[DuplicateItem]
class DashboardOut(BaseModel): total_files:int; total_storage:int; duplicate_files:int; duplicate_storage:int; potential_savings:int; largest_files:list[FileOut]; recent_uploads:list[FileOut]
