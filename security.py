from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from database import APIKey, get_db

api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Security(api_key_header), db: Session = Depends(get_db)):
    key = db.query(APIKey).filter(
        APIKey.key == api_key,
        APIKey.is_active == "true"
    ).first()

    if not key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    return key