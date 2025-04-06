from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.dbutils import get_db
from models.models import User
from core.config import Config


security = HTTPBearer()


def parse_supabase_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        token = credentials.credentials
        # Get header to find kid
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="Invalid token: missing kid")

        algorithm = headers.get("alg")
        if not algorithm or algorithm != "HS256":
            raise HTTPException(status_code=401, detail="Invalid token: unsupported algorithm")
        
        payload = jwt.decode(token, Config.SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        supabase_uid = payload.get("sub")
        if not supabase_uid:
            raise HTTPException(status_code=401, detail="Token missing subject")

        return payload

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


def get_current_user(
    payload: dict = Depends(parse_supabase_jwt),
    db: Session = Depends(get_db),
):
    supabase_uid = payload.get("sub")
    user = db.query(User).filter(User.supabase_uid == supabase_uid).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user