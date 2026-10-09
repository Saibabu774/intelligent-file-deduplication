# Intelligent File Deduplication & Storage Optimization System

Full-stack file management application with SHA-256 content hashing, duplicate grouping, storage analytics, safe deletion, deletion history, JWT authentication, Celery + Redis background hashing, MySQL, Alembic, React/Vite/TypeScript/MUI and Postman.

## Quick start with Docker
1. Copy `backend/.env.example` to `backend/.env` (already included for convenience).
2. Run `docker compose up --build`.
3. Backend Swagger: http://localhost:8000/docs
4. Frontend: http://localhost:5173
5. Demo login: `admin@example.com` / `Admin@123`

## Local backend
```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
python seed.py
uvicorn app.main:app --reload
```
Worker in another terminal:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
celery -A app.tasks.celery_app.celery worker --loglevel=info
```

## Local frontend
```powershell
cd frontend
npm install
npm run dev
```

## Architecture
Upload -> FastAPI streams file to disk -> creates DB record -> Celery task -> SHA-256 chunked hashing -> file_hashes -> duplicate_groups -> dashboard analytics.

## Security
JWT protected endpoints, per-user file ownership checks, extension allow-list, configurable upload size, protected-file deletion prevention, audit/deletion history, environment configuration, no full-file memory buffering.

## Testing
```powershell
cd backend
pytest -q
```

## Main endpoints
- POST `/api/v1/auth/register`
- POST `/api/v1/auth/login`
- POST `/api/v1/files/upload`
- GET `/api/v1/files`
- GET `/api/v1/files/{id}/download`
- DELETE `/api/v1/files/{id}`
- GET `/api/v1/duplicates/groups`
- GET `/api/v1/dashboard`
- GET `/api/v1/history/deletions`
