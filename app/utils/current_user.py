from fastapi import Request
from jose import jwt, JWTError
from app.utils.auth_helper import SECRET_KEY, ALGORITHM
from app.database import SessionLocal
from app.models.user import User

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        return None

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()

    return user
