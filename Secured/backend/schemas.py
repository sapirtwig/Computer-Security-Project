# from pydantic import BaseModel


# class RegisterRequest(BaseModel):
#     username: str
#     password: str
#     email: str


# class LoginRequest(BaseModel):
#     username: str
#     password: str

# class ClientSchema(BaseModel):
#     name: str
#     email: str
# schemas.py

from pydantic import BaseModel, EmailStr, constr
from typing import Annotated

# Schema for user registration with constraints
class RegisterRequest(BaseModel):
    username: Annotated[str, constr(strip_whitespace=True, min_length=3, max_length=50)]  # Must be 3-50 characters, no leading/trailing spaces
    password: Annotated[str, constr(min_length=10)]  # Must be at least 10 characters
    email: EmailStr  # Valid email format only

# Schema for login request (basic fields)
class LoginRequest(BaseModel):
    username: str
    password: str

# Schema for client data (name and email)
class ClientSchema(BaseModel):
    name: Annotated[str, constr(strip_whitespace=True, min_length=1, max_length=100)]  # Non-empty name, trimmed
    email: EmailStr  # Valid email format only


