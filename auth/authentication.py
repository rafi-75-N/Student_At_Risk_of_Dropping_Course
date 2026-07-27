import json
import os


DATABASE = "database/users.json"


ALLOWED_DOMAINS = (
    "@northsouth.edu",
    "@adminnorthsouth.edu",
    "@docnorthsouth.edu"
)


def load_users():

    if not os.path.exists(DATABASE):
        return []

    with open(DATABASE, "r") as file:
        return json.load(file)


def save_users(users):

    with open(DATABASE, "w") as file:
        json.dump(users, file, indent=4)


def register_user(name, email, password, confirm):

    # Empty fields
    if not name or not email or not password or not confirm:
        return False, "Please fill in all fields."

    # Email domain
    if not email.endswith(ALLOWED_DOMAINS):
        return False, "Please use a valid university email."

    # Passwords
    if password != confirm:
        return False, "Passwords do not match."

    users = load_users()

    # Existing account
    for user in users:

        if user["email"].lower() == email.lower():

            return False, "An account with this email already exists."

    users.append({

        "name": name,
        "email": email,
        "password": password

    })

    save_users(users)

    return True, "Account created successfully!"