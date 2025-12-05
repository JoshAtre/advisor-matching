from pydantic import BaseModel
from typing import Optional, List

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    username: str # OAuth2 standard uses 'username' for email
    password: str

# Profile Schemas
class ProfileUpdate(BaseModel):
    interests: str
    goals: str
    preferred_style: str

class UserOut(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    interests: Optional[str]
    goals: Optional[str]

    class Config:
        from_attributes = True

# Advisor Schemas
class AdvisorOut(BaseModel):
    id: int
    name: str
    department: str
    research_areas: str
    bio: str
    mentoring_style: str

    class Config:
        from_attributes = True

class MatchResult(BaseModel):
    advisor: AdvisorOut
    score: float
    explanation: str
