from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, expression

from .database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=expression.true(), unique=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
