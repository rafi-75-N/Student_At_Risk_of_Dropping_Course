import bcrypt

from api.db import SessionLocal
from api.models import User

ALLOWED_DOMAINS = {
    "@northsouth.edu": "instructor",
    "@adminnorthsouth.edu": "admin",
    "@docnorthsouth.edu": "doctor",
}


def get_role_from_email(email):
    """Returns 'instructor' / 'admin' / 'doctor', or None if the domain isn't recognized."""

    email = (email or "").lower()

    for domain, role in ALLOWED_DOMAINS.items():
        if email.endswith(domain):
            return role

    return None


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, password_hash):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def register_user(name, email, password, confirm):

    # Empty fields
    if not name or not email or not password or not confirm:
        return False, "Please fill in all fields."

    # Email domain -> role
    role = get_role_from_email(email)

    if role is None:
        return False, "Please use a valid university email."

    # Passwords
    if password != confirm:
        return False, "Passwords do not match."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    db = SessionLocal()

    try:
        existing = (
            db.query(User)
            .filter(User.email.ilike(email))
            .first()
        )

        if existing:
            return False, "An account with this email already exists."

        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=role,
        )

        db.add(user)
        db.commit()

        return True, "Account created successfully! You can now log in."

    finally:
        db.close()


def login_user(email, password):

    if not email or not password:
        return False, "Please enter your email and password."

    if get_role_from_email(email) is None:
        return False, "Invalid university email."

    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email.ilike(email))
            .first()
        )

        if not user:
            return False, "No account found with this email."

        if not verify_password(password, user.password_hash):
            return False, "Incorrect password."

        return True, {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }

    finally:
        db.close()