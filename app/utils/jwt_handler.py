from datetime import datetime, timedelta
from jose import jwt
from app.config.settings import settings
from typing import Dict, Any

def create_access_token(subject: Dict[str, Any], expires_minutes: int = None) -> str:
    if expires_minutes is None:
        expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    payload = subject.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload.update({"exp": expire_time})
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except Exception as exc:
        # Raise a generic exception and let the caller handle HTTP mapping
        raise
