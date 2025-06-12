from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.infra.db.session import get_db

router = APIRouter()


@router.get("/health", tags=["System"])
async def health_check(db: Session = Depends(get_db)):
    health_status = {"api_status": "ok", "db_status": "unknown"}
    try:
        db.execute(text("SELECT 1"))
        health_status["db_status"] = "ok"
    except Exception as e:
        health_status["db_status"] = "error"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_status,
        ) from e

    return JSONResponse(content=health_status)


# @router.get("/metrics", tags=["System"])
# async def metrics():
#     return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)>
