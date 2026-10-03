from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import CORS_ORIGINS, SERVICE_NAME
from app.database.connection import engine
from app.routers.api import api

app = FastAPI(title="Quản lý đồ án tốt nghiệp", version="1.0.0", description="REST API theo ranh giới SinhVien, DeTai và DangKy Service")
app.add_middleware(CORSMiddleware, allow_origins=[item.strip() for item in CORS_ORIGINS], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api)


@app.get("/health", tags=["Health"])
def health():
    try:
        with engine.connect() as connection: connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok", "service": SERVICE_NAME}
    except Exception:
        return {"status": "degraded", "database": "unavailable", "service": SERVICE_NAME}
