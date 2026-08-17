from fastapi import FastAPI

from .db import init_db
from .routers import auth, courses, assessments, admin

init_db()

app = FastAPI(title="Student Dropout Prediction API")

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(assessments.router)
app.include_router(admin.router)


@app.get("/")
def home():
    return {"message": "Student Dropout Prediction API is running!"}
