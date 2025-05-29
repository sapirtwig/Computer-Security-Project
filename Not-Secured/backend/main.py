import uvicorn
from fastapi import FastAPI
from routes import router
from database.mysql_db import create_tables
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Adding CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Including the router for handling API routes
app.include_router(router)

# Event triggered when the application starts
@app.on_event("startup")
def startup_event():
    create_tables()  # Create database tables if they do not exist

# Running the FastAPI server
if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=5000)
