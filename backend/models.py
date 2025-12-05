from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    
    # Profile Data
    interests = Column(Text, nullable=True) # JSON or comma-separated
    goals = Column(Text, nullable=True)
    preferred_style = Column(String, nullable=True)
    
    saved_advisors = relationship("SavedAdvisor", back_populates="user")

class Advisor(Base):
    __tablename__ = "advisors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    research_areas = Column(Text) # Main text for matching
    bio = Column(Text)
    mentoring_style = Column(String)

class SavedAdvisor(Base):
    __tablename__ = "saved_advisors"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    advisor_id = Column(Integer, ForeignKey("advisors.id"))
    
    user = relationship("User", back_populates="saved_advisors")
    advisor = relationship("Advisor")
