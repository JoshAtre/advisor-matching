import logging
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models, schemas, auth, matching, database
from database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdvisorMatch")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advisor Match V2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUTH ROUTES ---
@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": auth.create_access_token(data={"sub": user.email}), "token_type": "bearer"}

@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw, full_name=user.full_name)
    db.add(new_user)
    db.commit()
    return new_user

@app.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.put("/me/profile", response_model=schemas.UserOut)
def update_profile(profile: schemas.ProfileUpdate, 
                   current_user: models.User = Depends(auth.get_current_user),
                   db: Session = Depends(database.get_db)):
    current_user.interests = profile.interests
    current_user.goals = profile.goals
    current_user.preferred_style = profile.preferred_style
    db.commit()
    return current_user

# --- MATCHING ROUTES ---
@app.get("/matches", response_model=List[schemas.MatchResult])
def get_matches(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.interests:
        raise HTTPException(status_code=400, detail="Profile incomplete")

    advisors = db.query(models.Advisor).all()
    results = []
    
    for advisor in advisors:
        score, explanation = matching.generate_weighted_match(current_user, advisor)
        if score > 5: # Filter out noise
            results.append({"advisor": advisor, "score": score, "explanation": explanation})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

# --- REQUEST ROUTES (NEW) ---
@app.post("/requests", response_model=schemas.RequestOut)
def create_request(req: schemas.RequestCreate, 
                  current_user: models.User = Depends(auth.get_current_user), 
                  db: Session = Depends(database.get_db)):
    # Check for duplicate
    existing = db.query(models.MeetingRequest).filter_by(
        student_id=current_user.id, advisor_id=req.advisor_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Request already sent to this advisor")

    new_req = models.MeetingRequest(
        student_id=current_user.id,
        advisor_id=req.advisor_id,
        message=req.message,
        status="Pending"
    )
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req

@app.get("/requests", response_model=List[schemas.RequestOut])
def get_my_requests(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return db.query(models.MeetingRequest).filter(models.MeetingRequest.student_id == current_user.id).all()
