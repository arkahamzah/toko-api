from jose import JWTError, jwt
from fastapi import WebSocket, WebSocketDisconnect, status
from datetime import datetime, timedelta

SECRET_KEY = "rahasia-super-aman-ganti-di-production"
ALGORITHM = "HS256"

def buat_token(data: dict, expire_menit: int = 60):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_menit)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verifikasi_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
