from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Auth & User ---
class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    interests: Optional[str]
    goals: Optional[str]
    class Config:
        from_attributes = True

class ProfileUpdate(BaseModel):
    interests: str
    goals: str
    preferred_style: str

# --- Advisors ---
class AdvisorOut(BaseModel):
    id: int
    name: str
    department: str
    research_areas: str
    bio: str
    mentoring_style: str
    image_url: Optional[str] = None
    class Config:
        from_attributes = True

class MatchResult(BaseModel):
    advisor: AdvisorOut
    score: float
    explanation: str

# --- Requests ---
class RequestCreate(BaseModel):
    advisor_id: int
    message: str

class RequestOut(BaseModel):
    id: int
    status: str
    message: str
    created_at: datetime
    advisor: AdvisorOut
    class Config:
        from_attributes = True
