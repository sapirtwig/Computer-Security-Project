from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from schemas import LoginRequest, RegisterRequest, ClientSchema
from services import check_login, register_user, get_login_attempts, login_attempts, password_policy, password_recovery, \
    verify_recovery_code, change_current_password, add_client, get_clients_by_user
from database.mysql_db import get_db

router = APIRouter()

# Endpoint for user registration
@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)) -> JSONResponse:
    return register_user(
        username=request.username.strip(),
        password=request.password,
        email=request.email.strip(),
        db=db
    )

# Endpoint to get number of login attempts for a username
@router.get("/login_attempts/{username}")
def get_attempts(username: str) -> JSONResponse:
    attempts = get_login_attempts(username)
    return JSONResponse(content={"username": username, "login_attempts": attempts}, status_code=200)

# Endpoint for user login, includes brute-force protection
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)) -> JSONResponse:
    max_attempts = password_policy['LoginAttempts']
    current_attempts = login_attempts.get(request.username, 0)

    # Check if user is already locked out
    if current_attempts >= max_attempts:
        return JSONResponse(
            content={"message": "Account is locked. Too many login attempts."},
            status_code=403
        )

    is_valid = check_login(username=request.username, password=request.password, db=db)
    if is_valid:
        return JSONResponse(content={"message": "Login successful"}, status_code=200)

    # Calculate remaining attempts after the failed attempt
    remaining_attempts = max_attempts - login_attempts.get(request.username, 0)
    if remaining_attempts <= 0:
        return JSONResponse(
            content={"message": "Account is now locked. Too many login attempts."},
            status_code=403
        )
    
    return JSONResponse(
        content={"message": f"Invalid username or password. {remaining_attempts} attempts remaining."},
        status_code=401
    )

# Endpoint to start password recovery by email
@router.post("/forgot_password")
def forgot_password(email: str, db: Session = Depends(get_db)) -> JSONResponse:
    return password_recovery(email=email.strip(), db=db)

# Endpoint to change password using verification code sent by email
@router.post("/change_password_with_verify_code")
def change_password_with_verify_code(recovery_code: str, email: str, new_password: str, db: Session = Depends(get_db)) -> JSONResponse:
    if verify_recovery_code(recovery_code=recovery_code, email=email):
        return change_current_password(email=email, new_password=new_password, db=db)
    return JSONResponse(status_code=401, content={"message": "Invalid recovery code."})

# Endpoint to change password directly (e.g., for logged-in user)
@router.post("/change_password")
def change_password(email: str, new_password: str, db: Session = Depends(get_db)) -> JSONResponse:
    return change_current_password(email=email, new_password=new_password, db=db)

# Endpoint to add a new client associated with a user
@router.post("/add_client")
def add_new_client(user_id: int, client: ClientSchema , db: Session = Depends(get_db)) -> JSONResponse:
    # ⚠️ In production, user_id should come from an authenticated token/session
    return add_client(user_id=user_id, client=client, db=db)

# Endpoint to retrieve clients of a specific user
@router.get("/get_user_clients")
def get_user_clients(user_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    return get_clients_by_user(user_id=user_id, db=db)