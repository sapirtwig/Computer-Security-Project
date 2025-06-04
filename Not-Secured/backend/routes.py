from services import reset_login_attempts
from services import add_client_db
from fastapi import APIRouter, Depends, Body
from starlette.responses import JSONResponse
from database.mysql_db import get_db, get_db_connection
from schemas import LoginRequest
from services import check_login, get_login_attempts, login_attempts, password_policy, password_recovery, \
    verify_recovery_code, change_current_password
from fastapi.responses import HTMLResponse

router = APIRouter()

from services import register_user


@router.post("/register")
def register_user_endpoint(
        username: str = Body(...),
        password: str = Body(...),
        email: str = Body(...)
):
    # Calling register_user function, which executes a raw SQL query (SQL Injection risk)
    return register_user(username=username, password=password, email=email)


# API endpoint to retrieve the number of failed login attempts for a user
@router.get("/login_attempts/{username}")
def get_attempts(username: str) -> JSONResponse:
    attempts = get_login_attempts(username)
    return JSONResponse(content={"username": username, "login_attempts": attempts}, status_code=200)


@router.post("/login")
def login(request: LoginRequest) -> JSONResponse:
    max_attempts = password_policy['LoginAttempts']

    if get_login_attempts(request.username) >= max_attempts:
        return JSONResponse(
            content={"message": "User is locked due to too many failed attempts."},
            status_code=401  # Unauthorized
        )

    is_valid = check_login(username=request.username, password=request.password)

    if is_valid:
        return JSONResponse(content={"message": "Login successful"}, status_code=200)

    remaining_attempts = max_attempts - login_attempts.get(request.username, 0)
    return JSONResponse(
        content={"message": f"Invalid username or password. {remaining_attempts} attempts remaining."},
        status_code=401
    )


@router.post("/forgot_password")
def forgot_password(email: str) -> JSONResponse:
    response = password_recovery(email=email)

    # Reset login attempts for the user associated with the email
    connection = get_db_connection()
    cursor = connection.cursor()

    # Vulnerability: SQL Injection Risk
    # User input (email) is inserted directly into the SQL query without sanitization.
    # An attacker could inject malicious SQL to retrieve or manipulate user data.
    query = f"SELECT username FROM users WHERE email = '{email}'"
    cursor.execute(query)  # Unsafe query execution
    user = cursor.fetchone()

    if user:
        reset_login_attempts(user[0])

    connection.close()
    return response


@router.post("/change_password_with_verify_code")
def change_password_with_verify_code(recovery_code: str, email: str, new_password: str) -> JSONResponse:
    if verify_recovery_code(recovery_code=recovery_code, email=email):
        return change_current_password(email=email, new_password=new_password)
    return JSONResponse(status_code=401, content={"message": "Invalid recovery code."})


@router.post("/change_password")
def change_password(email: str, new_password: str) -> JSONResponse:
    # Calling change_current_password function, which executes a raw SQL query (SQL Injection risk)
    return change_current_password(email=email, new_password=new_password)


from pydantic import BaseModel


class ClientRequest(BaseModel):
    name: str
    email: str


@router.post("/add_client")
def add_client_endpoint(
        name: str = Body(...),
        email: str = Body(...)
):
    # Calling add_client_db function, which executes a raw SQL query (SQL Injection risk)
    return add_client_db(name=name, email=email)


@router.get("/get_user_clients")
async def get_user_clients(user_id: int, db=Depends(get_db)):
    try:
        cursor = db.cursor()

        # Vulnerability: SQL Injection Risk
        # User input (user_id) is inserted directly into the SQL query without sanitization.
        # An attacker could inject malicious SQL to retrieve or manipulate user data.
        query = f"SELECT name, email FROM clients WHERE user_id = {user_id}"
        cursor.execute(query)  # Unsafe query execution
        clients = cursor.fetchall()
        cursor.close()
        response_content = "<br>".join([f"{client[0]} - {client[1]}" for client in clients])
        return HTMLResponse(content=response_content, status_code=200)
 # Return JSON instead of HTML
        # return JSONResponse(
        #     content={"clients": [{"name": client[0], "email": client[1]} for client in clients]},
        #     status_code=200
        # )
        # # Generate an HTML response to display client data
        # response_content = "<br>".join([f"{client[0]} - {client[1]}" for client in clients])
        # return HTMLResponse(content=response_content, status_code=200)

    except Exception as e:
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"},
            status_code=500
        )
