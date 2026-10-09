from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "Intelligent File Deduplication System"
    environment: str = "development"
    secret_key: str = "change-this-secret-key"
    access_token_expire_minutes: int = 120
    database_url: str = "mysql+pymysql://root:password@localhost:3306/file_dedup_db"
    redis_url: str = "redis://localhost:6379/0"
    storage_dir: str = "./storage"
    max_upload_size_mb: int = 5120
    allowed_extensions: str = "pdf,txt,csv,jpg,jpeg,png,gif,webp,doc,docx,xls,xlsx,ppt,pptx,zip,rar,mp3,mp4"
    cors_origins: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    @property
    def allowed_ext_set(self): return {x.strip().lower() for x in self.allowed_extensions.split(',')}
    @property
    def cors_list(self): return [x.strip() for x in self.cors_origins.split(',')]
settings = Settings()
