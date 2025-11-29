from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
import re
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from database import engine, get_db
from models import Base, User
from auth import create_access_token, verify_password, get_user_by_email

app = FastAPI()

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Email validation regex
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Args:
        user: UserCreate model with email and password
        db: Database session dependency
        
    Returns:
        UserResponse: Created user's id and email
        
    Raises:
        HTTPException: 400 if email is invalid or already exists
    """
    # Validate email format
    if not re.match(EMAIL_REGEX, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    # Check if user already exists
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = pwd_context.hash(user.password)
    
    # Create user in database
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.
    
    Args:
        form_data: OAuth2PasswordRequestForm with username (email) and password
        db: Database session dependency
        
    Returns:
        dict: Access token and token type
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    user = get_user_by_email(db, form_data.username)
    
    # Validate credentials
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}