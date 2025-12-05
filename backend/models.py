from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    
    # Profile Data
    interests = Column(Text, nullable=True)
    goals = Column(Text, nullable=True)
    preferred_style = Column(String, nullable=True)
    
    saved_advisors = relationship("SavedAdvisor", back_populates="user")
    requests = relationship("MeetingRequest", back_populates="student")

class Advisor(Base):
    __tablename__ = "advisors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    research_areas = Column(Text)
    bio = Column(Text)
    mentoring_style = Column(String)
    image_url = Column(String, nullable=True) # Added for UI polish

class SavedAdvisor(Base):
    __tablename__ = "saved_advisors"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    advisor_id = Column(Integer, ForeignKey("advisors.id"))
    
    user = relationship("User", back_populates="saved_advisors")
    advisor = relationship("Advisor")

class MeetingRequest(Base):
    __tablename__ = "meeting_requests"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    advisor_id = Column(Integer, ForeignKey("advisors.id"))
    status = Column(String, default="Pending") # Pending, Accepted, Declined
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("User", back_populates="requests")
    advisor = relationship("Advisor")
