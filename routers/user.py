from fastapi import APIRouter

router = APIRouter()

@router.post("/create")
def create_user():
    return {"message": "User created"}