from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models.task import User
from app.schemas.task import UserCreate, User as UserSchema
from app.database.database import get_session
from app.core.auth import get_password_hash, authenticate_user, create_access_token
from datetime import timedelta
import uuid

router = APIRouter()

@router.post("/register", response_model=UserSchema)
def register_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.
    """
    try:
        # Check if user already exists
        statement = select(User).where(User.email == user_create.email)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,  # Changed to 409 Conflict
                detail="Email already registered"
            )

        # Create new user with hashed password
        hashed_password = get_password_hash(user_create.password)
        user = User(
            email=user_create.email,
            password=hashed_password
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user
    except HTTPException:
        # Re-raise HTTP exceptions to maintain proper status codes
        raise
    except Exception as e:
        # Handle any other validation errors
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


@router.post("/signup", response_model=UserSchema)
def signup_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Signup a new user (alias for register).
    """
    return register_user(user_create, session)


@router.post("/login")
def login_user(user_create: UserCreate, session: Session = Depends(get_session)):
    """
    Authenticate user and return access token.
    """
    try:
        statement = select(User).where(User.email == user_create.email)
        user = session.exec(statement).first()

        if not user or not authenticate_user(user, user_create.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions to maintain proper status codes
        raise
    except Exception as e:
        # Handle any other validation errors
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )