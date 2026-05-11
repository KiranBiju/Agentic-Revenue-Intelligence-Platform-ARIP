from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import SessionLocal
from app.core.redis_client import redis_client

router = APIRouter()


@router.get("/health")
def health_check():
    db_ok = False
    redis_ok = False

    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    finally:
        db.close()

    try:
        redis_client.ping()
        redis_ok = True
    except Exception:
        redis_ok = False

    overall = "healthy" if db_ok and redis_ok else "degraded"

    return {
        "status": overall,
        "database": db_ok,
        "redis": redis_ok,
    }