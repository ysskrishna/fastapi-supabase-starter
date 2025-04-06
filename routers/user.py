from fastapi import APIRouter, Depends, HTTPException
from core.jwtutils import parse_supabase_jwt, get_current_user
from sqlalchemy.orm import Session
from core.dbutils import get_db
from models.models import User

router = APIRouter()

@router.post("/create")
def create_user(token_payload: dict = Depends(parse_supabase_jwt), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.supabase_uid == token_payload["sub"]).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        supabase_uid=token_payload["sub"],
        email=token_payload.get("email", "")
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "User created successfully",
        "user_id": new_user.user_id,
        "email": new_user.email
    }

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }