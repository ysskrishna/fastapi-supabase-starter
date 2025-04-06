import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")
    SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
    DATABASE_URL = os.getenv("DATABASE_URL")
