from fastapi import APIRouter, Depends
from core.jwtutils import parse_supabase_jwt, get_current_user
from sqlalchemy.orm import Session
from core.dbutils import get_db
from models.models import User

router = APIRouter()

@router.post("/create")
def create_user(token_payload: dict = Depends(parse_supabase_jwt), db: Session = Depends(get_db)):
    print(token_payload)
    return {"message": "User created"}

@router.get("/me")
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    print(current_user)
    return {"message": "User read"}