from sqlalchemy import  Column, String, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_mixin
from core.dbutils import Base
import uuid

@declarative_mixin
class Timestamp:
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class User(Timestamp, Base):
    __tablename__ ="users"

    user_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    supabase_uid = Column(String, index=True, nullable=False)
    email = Column(String, nullable=False)