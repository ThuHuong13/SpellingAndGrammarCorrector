from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserLogin, UserCreate
from auth import hash_password, verify_password, create_access_token

router = APIRouter(tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return JSONResponse(
            status_code=400, content={"message": "Usename already exists."}
        )

    # Hash the password and create a new user
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return JSONResponse(
        status_code=201, content={"message": "User created successfully."}
    )


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        return JSONResponse(
            status_code=400, content={"message": "Invalid credentials."}
        )

    token, expire = create_access_token({"sub": str(db_user.id)})
    return JSONResponse(
        status_code=200,
        content={"access_token": token, "token_type": "bearer", "expire": str(expire)},
    )
