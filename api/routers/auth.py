from fastapi import APIRouter

from ..db import SessionLocal
from ..models import User
from ..security import get_role_from_email, hash_password, verify_password
from ..schemas import RegisterRequest, LoginRequest, AuthResponse, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest):

    if not payload.name or not payload.email or not payload.password or not payload.confirm:
        return AuthResponse(success=False, message="Please fill in all fields.")

    role = get_role_from_email(payload.email)

    if role is None:
        return AuthResponse(success=False, message="Please use a valid university email.")

    if payload.password != payload.confirm:
        return AuthResponse(success=False, message="Passwords do not match.")

    if len(payload.password) < 6:
        return AuthResponse(success=False, message="Password must be at least 6 characters.")

    db = SessionLocal()

    try:
        existing = db.query(User).filter(User.email.ilike(payload.email)).first()

        if existing:
            return AuthResponse(success=False, message="An account with this email already exists.")

        user = User(
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password),
            role=role,
        )

        db.add(user)
        db.commit()

        return AuthResponse(success=True, message="Account created successfully! You can now log in.")

    finally:
        db.close()


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):

    if not payload.email or not payload.password:
        return AuthResponse(success=False, message="Please enter your email and password.")

    if get_role_from_email(payload.email) is None:
        return AuthResponse(success=False, message="Invalid university email.")

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email.ilike(payload.email)).first()

        if not user:
            return AuthResponse(success=False, message="No account found with this email.")

        if not verify_password(payload.password, user.password_hash):
            return AuthResponse(success=False, message="Incorrect password.")

        return AuthResponse(success=True, user=UserOut.model_validate(user))

    finally:
        db.close()
