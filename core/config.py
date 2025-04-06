import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")
