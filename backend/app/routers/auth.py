import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from app.database import get_db
from app.models import User
from app.schemas import TokenResponse
from app.auth import create_access_token

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")

router = APIRouter(prefix="/auth", tags=["auth"])


class GoogleTokenRequest:
    def __init__(self, credential: str):
        self.credential = credential

from pydantic import BaseModel

class GoogleTokenBody(BaseModel):
    credential: str


@router.post("/google", response_model=TokenResponse)
def google_login(body: GoogleTokenBody, db: Session = Depends(get_db)):
    try:
        info = id_token.verify_oauth2_token(
            body.credential,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Invalid Google token: {e}")

    email = info.get("email", "")
    if not email.endswith("@tcd.ie"):
        raise HTTPException(status_code=403, detail="Only @tcd.ie accounts are allowed")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)

    return TokenResponse(access_token=create_access_token(user.id))
