# from sqlalchemy.orm import declarative_base
# from sqlalchemy import Column, String, Integer, ForeignKey

# Base = declarative_base()


# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     username = Column(String(255), unique=True, index=True)
#     email = Column(String(255), unique=True, index=True)
#     password = Column(String(255), index=True)

# class Client(Base):
#     __tablename__ = 'client'
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
#     name = Column(String(255), index=True)
#     email = Column(String(255), index=True)
# models.py
# models.py

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Text

# Base class for all models
Base = declarative_base()

# User table definition
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, index=True)       # Unique username
    email = Column(String(255), unique=True, index=True)          # Unique email
    password = Column(String(255), index=True)                    # Encrypted password
    password_history = Column(Text, default="[]")                 # JSON string to store previous passwords

# Client table definition
class Client(Base):
    __tablename__ = 'client'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))  # Linked to a user
    name = Column(String(255), index=True)
    email = Column(String(255), index=True)

