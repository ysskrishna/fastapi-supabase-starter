import time
from typing import Optional, Dict
import requests
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.dbutils import get_db
from models.models import User
from core.config import Config

class JWKSCache:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.jwks_url = f"https://{project_id}.supabase.co/auth/v1/keys"
        self._jwks_cache: Optional[Dict] = None
        self._jwks_cache_expiry: float = 0

    def get_jwks(self, force_refresh=False) -> Dict:
        now = time.time()
        if not self._jwks_cache or now > self._jwks_cache_expiry or force_refresh:
            resp = requests.get(self.jwks_url)
            resp.raise_for_status()
            self._jwks_cache = resp.json()
            self._jwks_cache_expiry = now + 15 * 60  # cache 15 minutes
        return self._jwks_cache

# Instantiate JWKSCache once globally
jwks_cache = JWKSCache(Config.SUPABASE_PROJECT_ID)
security = HTTPBearer()


def parse_supabase_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    try:
        token = credentials.credentials
        # Get header to find kid
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="Invalid token: missing kid")

        # Get JWKS keys
        jwks = jwks_cache.get_jwks()
        key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

        # If key not found, refresh cache once and retry
        if not key and time.time() > jwks_cache._jwks_cache_expiry:
            jwks = jwks_cache.get_jwks(force_refresh=True)
            key = next((k for k in jwks["keys"] if k["kid"] == kid), None)

        if not key:
            raise HTTPException(status_code=401, detail="Invalid token: unknown kid")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)

        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"]
        )

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