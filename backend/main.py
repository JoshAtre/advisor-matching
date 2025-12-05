import logging
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models, schemas, auth, matching, database
from database import engine

# 1. Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdvisorMatch")

# 2. Init DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Advisor Match MVP")

# 3. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw, full_name=user.full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"event=user_signup user_id={new_user.id}")
    return new_user

@app.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.put("/me/profile", response_model=schemas.UserOut)
def update_profile(profile: schemas.ProfileUpdate, 
                   current_user: models.User = Depends(auth.get_current_user),
                   db: Session = Depends(database.get_db)):
    current_user.interests = profile.interests
    current_user.goals = profile.goals
    current_user.preferred_style = profile.preferred_style
    db.commit()
    db.refresh(current_user)
    logger.info(f"event=onboarding_completed user_id={current_user.id}")
    return current_user

@app.get("/matches", response_model=List[schemas.MatchResult])
def get_matches(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    # Failure Handling: Missing Profile
    if not current_user.interests:
        raise HTTPException(status_code=400, detail="Please complete your profile first.")

    advisors = db.query(models.Advisor).all()
    if not advisors:
        logger.warning("event=match_requested result=no_advisors_found")
        return []

    results = []
    user_text = f"{current_user.interests} {current_user.goals} {current_user.preferred_style}"

    for advisor in advisors:
        advisor_text = f"{advisor.research_areas} {advisor.mentoring_style} {advisor.bio}"
        score, explanation = matching.generate_match(user_text, advisor_text)
        
        # Only return decent matches
        if score > 0:
            results.append({
                "advisor": advisor,
                "score": score,
                "explanation": explanation
            })

    # Sort by score desc
    results.sort(key=lambda x: x["score"], reverse=True)
    
    logger.info(f"event=match_results_viewed user_id={current_user.id} count={len(results)}")
    return results

@app.post("/advisors/{advisor_id}/save")
def save_advisor(advisor_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    exists = db.query(models.SavedAdvisor).filter_by(user_id=current_user.id, advisor_id=advisor_id).first()
    if not exists:
        saved = models.SavedAdvisor(user_id=current_user.id, advisor_id=advisor_id)
        db.add(saved)
        db.commit()
        logger.info(f"event=advisor_saved user_id={current_user.id} advisor_id={advisor_id}")
    return {"status": "saved"}

@app.get("/saved", response_model=List[schemas.AdvisorOut])
def get_saved_advisors(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    saved = db.query(models.SavedAdvisor).filter(models.SavedAdvisor.user_id == current_user.id).all()
    return [s.advisor for s in saved]
