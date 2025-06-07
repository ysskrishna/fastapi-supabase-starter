from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import user
from core.dbutils import engine
from models import models

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Supabase Starter API"}

app.include_router(user.router, prefix="/user", tags=["user"])

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
