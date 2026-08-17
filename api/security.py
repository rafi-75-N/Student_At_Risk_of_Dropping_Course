import bcrypt

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
