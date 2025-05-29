# import random
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# from sqlalchemy.orm import Session
# from starlette.responses import JSONResponse

# from schemas import ClientSchema
# from database.models import User, Client
# from utils import encrypt_password, is_password_valid

# # login with policy password
# from utils import load_password_policy
# from configuration import *

# # Load the password policy from the ini file
# password_policy = load_password_policy()


# def check_login(username: str, password: str, db: Session) -> bool:
#     max_attempts = password_policy['LoginAttempts']  # Load the max login attempts from policy

#     # Check if the user has exceeded the max attempts
#     if username in login_attempts and login_attempts[username] >= max_attempts:
#         print(f"User {username} is locked due to too many login attempts.")
#         return False  # Account is locked

#     hashed_password = encrypt_password(password)  # Encrypt the provided password
#     user = db.query(User).filter(User.username == username, User.password == hashed_password).first()

#     if user:
#         reset_login_attempts(username)  # Reset attempts on successful login
#         return True

#     # Increment failed attempts
#     increment_login_attempts(username)
#     remaining_attempts = max_attempts - login_attempts[username]
#     print(f"Invalid login. {remaining_attempts} attempts remaining for {username}.")
#     return False


# login_attempts = {}  # Dictionary to track login attempts for each user
# email_to_recovery_password = {}


# def get_login_attempts(username: str) -> int:
#     """
#     Get the current number of failed login attempts for a specific user.
#     """
#     return login_attempts.get(username, 0)


# def reset_login_attempts(username: str):
#     """
#     Reset the login attempts counter for a user.
#     """
#     if username in login_attempts:
#         login_attempts.pop(username)


# def increment_login_attempts(username: str):
#     """
#     Increment the login attempts counter for a user.
#     """
#     login_attempts[username] = login_attempts.get(username, 0) + 1


# def register_user(username: str, password: str, email: str, db: Session) -> JSONResponse:
#     try:
#         existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
#         if existing_user:
#             return JSONResponse(
#                 status_code=400,
#                 content={"message": "Username or email already exists"}
#             )

#         # Validate password
#         if not is_password_valid(password, password_policy):
#             return JSONResponse(
#                 status_code=400,
#                 content={"message": (
#             "Password does not meet the security requirements. "
#             "Make sure your password includes at least one uppercase letter, "
#             "one lowercase letter, one digit, and one special character (e.g., !@#$%^&*)."
#         )}
#             )

#         # Create new user
#         user = User(
#             username=username,
#             email=email,
#             password=encrypt_password(password)
#         )
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#         return JSONResponse(
#             status_code=201,
#             content={"message": "User registered successfully"}
#         )

#     except Exception as e:
#         print(e)
#         return JSONResponse(
#             status_code=400,
#             content={"message": "Something went wrong"}
#         )


# # Function to generate a 6-digit recovery code
# def generate_recovery_code():
#     return encrypt_password(str(random.randint(100000, 999999)))


# def password_recovery(email: str, db : Session):
#     if not db.query(User).filter((User.email == email)).first():
#         return False
#     recovery_code = generate_recovery_code()
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = email
#     message["Subject"] = "Your Recovery Password"
#     message.attach(MIMEText(f"Your recovery password is: {recovery_code}", "plain"))
#     try:
#         # Establish connection to the SMTP server
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()  # Secure the connection
#             server.login(sender_email, sender_password)
#             server.send_message(message)
#             print(f"Recovery email sent to {email}")
#             email_to_recovery_password[email.lower()] = recovery_code
#             return JSONResponse(status_code=200, content={"message": "Recovery password sent successfully"})
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         return JSONResponse(status_code=400, content={"message": "Something went wrong"})


# def verify_recovery_code(recovery_code: str, email: str):
#     if email_to_recovery_password.get(email.lower()) == recovery_code:
#         return True
#     return False


# def change_current_password(email: str, new_password: str, db: Session):
#     if is_password_valid(new_password, password_policy):
#         try:
#             user = db.query(User).filter(User.email == email).first()
#             user.password = encrypt_password(new_password)
#             db.commit()
#             email_to_recovery_password.pop(email, None)
#             return JSONResponse(status_code=200, content={"message": "Password changed successfully"})
#         except Exception as e:
#             print(e)
#             return JSONResponse(status_code=400, content={"message": "Something went wrong"})
#     return JSONResponse(status_code=400, content={"message": "Weak password"})


# def add_client(client: ClientSchema, user_id: int, db: Session):
#     if not db.query(Client).filter(Client.email == client.email).first():
#         new_client = Client(user_id=user_id, name=client.name, email=client.email)
#         db.add(new_client)
#         db.commit()
#         db.refresh(new_client)
#         return JSONResponse(status_code=200, content={"message": "Client added successfully"})
#     return JSONResponse(status_code=400, content={"message": "Client already exists"})

# def get_clients_by_user(user_id: int, db: Session):
#     return db.query(Client).filter(Client.user_id == user_id).all()
# services.py

import hashlib
import json
import os
import re
import smtplib
from cryptography.hazmat.primitives import hashes, hmac
from email.mime.text import MIMEText
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from database.models import User, Client
from configuration import smtp_server, smtp_port, sender_email, sender_password, subject
from utils import load_password_policy

password_policy = load_password_policy()

# Keeps track of failed login attempts per user
login_attempts = {}

# Stores recovery codes per email (in-memory)
recovery_codes = {}  # {email: "123456"}

# Load weak passwords dictionary
with open("dictionary.txt", "r") as f:
    dictionary_words = set(word.strip().lower() for word in f)

# Hash password using HMAC with salt
def hash_password(password: str, salt: str = "mysalt") -> str:
    h = hmac.HMAC(salt.encode(), hashes.SHA256())
    h.update(password.encode())
    return h.finalize().hex()

# Validate password complexity rules
def is_password_complex(password: str) -> bool:
    rules = password_policy.get("Complexity", [])

    if "Uppercase" in rules and not re.search(r"[A-Z]", password):
        return False
    if "Lowercase" in rules and not re.search(r"[a-z]", password):
        return False
    if "Digits" in rules and not re.search(r"\d", password):
        return False
    if "SpecialCharacters" in rules and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# Check if password appears in dictionary of weak words
def is_password_in_dictionary(password: str) -> bool:
    return password.lower() in dictionary_words

# Get password history from DB-stored JSON
def get_password_history(user: User) -> list:
    return json.loads(user.password_history or "[]")

# Update password history (keep only N most recent passwords)
def update_password_history(user: User, new_password: str):
    history = get_password_history(user)
    history.insert(0, new_password)
    max_history = int(password_policy.get("HistoryLimit", 3))
    user.password_history = json.dumps(history[:max_history])

# Check if email is in valid format
def is_valid_email(email: str) -> bool:
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None

# Handle user registration
def register_user(username: str, password: str, email: str, db: Session) -> JSONResponse:
    if not is_valid_email(email):
        return JSONResponse(status_code=400, content={"message": "Invalid email format."})
    if len(password) < int(password_policy.get("PasswordLength", 10)):
        return JSONResponse(status_code=400, content={"message": "Password too short."})
    if not is_password_complex(password):
        return JSONResponse(status_code=400, content={"message": "Password must be more complex."})
    if is_password_in_dictionary(password):
        return JSONResponse(status_code=400, content={"message": "Password is too weak."})

    hashed_password = hash_password(password)
    user = User(username=username, email=email, password=hashed_password)
    db.add(user)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "User registered successfully."})

# Handle login logic
def check_login(username: str, password: str, db: Session) -> bool:
    user = db.query(User).filter_by(username=username).first()
    if not user:
        return False

    if username not in login_attempts:
        login_attempts[username] = 0

    hashed_input = hash_password(password)
    if hashed_input == user.password:
        login_attempts[username] = 0
        return True

    login_attempts[username] += 1
    return False

# Return current failed login attempts for user
def get_login_attempts(username: str) -> int:
    return login_attempts.get(username, 0)

# Start password recovery process
def password_recovery(email: str, db: Session) -> JSONResponse:
    if not is_valid_email(email):
        return JSONResponse(status_code=400, content={"message": "Invalid email format."})

    user = db.query(User).filter_by(email=email).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "Email not found."})

    import random
    recovery_code = str(random.randint(100000, 999999))
    recovery_codes[email] = recovery_code

    try:
        msg = MIMEText(f"Your recovery code is: {recovery_code}")
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        return JSONResponse(status_code=200, content={"message": "Recovery code sent to your email."})
    except Exception:
        return JSONResponse(status_code=500, content={"message": "Failed to send recovery email."})

# Check if recovery code is correct
def verify_recovery_code(recovery_code: str, email: str) -> bool:
    return recovery_codes.get(email) == recovery_code

# Change user password (after recovery or direct change)
def change_current_password(email: str, new_password: str, db: Session) -> JSONResponse:
    if not is_valid_email(email):
        return JSONResponse(status_code=400, content={"message": "Invalid email format."})

    user = db.query(User).filter_by(email=email).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found."})

    if len(new_password) < int(password_policy.get("PasswordLength", 10)):
        return JSONResponse(status_code=400, content={"message": "Password too short."})
    if not is_password_complex(new_password):
        return JSONResponse(status_code=400, content={"message": "Password must be more complex."})
    if is_password_in_dictionary(new_password):
        return JSONResponse(status_code=400, content={"message": "Password is too weak."})

    hashed_new = hash_password(new_password)
    if hashed_new in get_password_history(user):
        return JSONResponse(status_code=400, content={"message": "Password was used recently. Choose another."})

    user.password = hashed_new
    update_password_history(user, hashed_new)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Password changed successfully."})

# Add new client entry to DB
def add_client(user_id: int, client: Client, db: Session) -> JSONResponse:
    new_client = Client(user_id=user_id, name=client.name, email=client.email)
    db.add(new_client)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Client added successfully."})

# Get all clients associated with a user
def get_clients_by_user(user_id: int, db: Session) -> JSONResponse:
    clients = db.query(Client).filter_by(user_id=user_id).all()
    return JSONResponse(content={"clients": [{"name": c.name, "email": c.email} for c in clients]})
