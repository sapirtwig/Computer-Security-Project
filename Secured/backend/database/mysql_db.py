# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from database.models import Base

# # MySQL connection details
# mysql_user = 'root'
# mysql_password = 'password'
# mysql_host = 'mysql'
# mysql_database = 'project'
# mysql_port = '3306'  # Default MySQL port

# # Create the connection string for SQLAlchemy
# connection_string = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}'

# # Create the engine (this is the connection to the database)
# engine = create_engine(connection_string)

# # Create a configured "Session" class
# SessionLocal = sessionmaker(autocommit=False ,autoflush=False, bind=engine)

# def create_tables():
#     Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# mysql_db.py

import env_loader  # Loads environment variables from .env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME  # Import config values

# Create the connection string securely using environment variables
connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Attempt to create the SQLAlchemy engine (connects to the database)
try:
    engine = create_engine(connection_string)
except Exception as e:
    raise ConnectionError(f"Could not connect to the database: {e}")

# Create a session class bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This function creates all tables based on the models defined in models.py
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency used in FastAPI routes to access the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

