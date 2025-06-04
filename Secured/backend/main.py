import uvicorn
from fastapi import FastAPI
from routes import router
from database.mysql_db import create_tables
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # כתובת ה-Frontend
    allow_credentials=True,
    allow_methods=["*"],  # we can restrict the methods by stating wich method we want (allow_methods=["GET", "POST", "PUT", "DELETE"])
    allow_headers=["*"],  # we can restrict the headers by stating wich headers we want ( allow_headers=["Authorization", "Content-Type"])
) 

load_dotenv()


app.include_router(router)

@app.on_event("startup")
def startup_event():
    create_tables()


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=5000)


