import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:password@127.0.0.1:3306/demo_quan_ly_do_an?charset=utf8mb4"
)
SINHVIEN_SERVICE_URL = os.getenv("SINHVIEN_SERVICE_URL", "http://127.0.0.1:8001/api/v1")
DETAI_SERVICE_URL = os.getenv("DETAI_SERVICE_URL", "http://127.0.0.1:8002/api/v1")
SERVICE_NAME = os.getenv("SERVICE_NAME", "all")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:4200,http://127.0.0.1:4200").split(",")
