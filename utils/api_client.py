"""
Thin HTTP client for the FastAPI backend. Every Streamlit view that used
to talk to Postgres directly now goes through the functions in here.
Requires the API server running (uvicorn api.main:app) alongside Streamlit.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def _get(path, params=None):
    response = requests.get(f"{API_BASE_URL}{path}", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def _post(path, json_body=None, params=None):
    response = requests.post(f"{API_BASE_URL}{path}", json=json_body, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def _put(path, json_body=None, params=None):
    response = requests.put(f"{API_BASE_URL}{path}", json=json_body, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def _delete(path, params=None):
    response = requests.delete(f"{API_BASE_URL}{path}", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


# ---------- Auth ----------

def register_user(name, email, password, confirm):
    result = _post("/auth/register", {"name": name, "email": email, "password": password, "confirm": confirm})
    return result["success"], result["message"]


def login_user(email, password):
    result = _post("/auth/login", {"email": email, "password": password})
    if result["success"]:
        return True, result["user"]
    return False, result["message"]


# ---------- Courses ----------

def create_course(course_name, section, semester, instructor_id):
    return _post("/courses", {
        "course_name": course_name,
        "section": section,
        "semester": semester,
        "instructor_id": instructor_id,
    })


def list_courses(instructor_id=None):
    params = {"instructor_id": instructor_id} if instructor_id is not None else None
    return _get("/courses", params=params)


def list_enrollments(course_id):
    return _get(f"/courses/{course_id}/enrollments")


def upsert_enrollment(course_id, student_id, student_name, student_email,
                       midterm_score, assignments_avg, quizzes_avg,
                       participation_score, projects_score):
    return _post("/courses/enrollments", {
        "course_id": course_id,
        "student_id": student_id,
        "student_name": student_name,
        "student_email": student_email,
        "midterm_score": midterm_score,
        "assignments_avg": assignments_avg,
        "quizzes_avg": quizzes_avg,
        "participation_score": participation_score,
        "projects_score": projects_score,
    })


def remove_enrollment(course_id, student_id):
    return _delete(f"/courses/{course_id}/enrollments/{student_id}")


# ---------- Assessments ----------

def create_assessment(student_id, student_name, doctor_id, attendance, study_hours, sleep_hours, stress_level):
    return _post("/assessments", {
        "student_id": student_id,
        "student_name": student_name,
        "doctor_id": doctor_id,
        "attendance": attendance,
        "study_hours": study_hours,
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
    })


def search_latest_assessment(student_id):
    return _get("/assessments/search", params={"student_id": student_id})


def update_assessment(assessment_id, student_name, attendance, study_hours, sleep_hours, stress_level):
    return _put(f"/assessments/{assessment_id}", {
        "student_name": student_name,
        "attendance": attendance,
        "study_hours": study_hours,
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
    })


def delete_assessment(assessment_id):
    return _delete(f"/assessments/{assessment_id}")


def assessment_history(doctor_id):
    return _get("/assessments/history", params={"doctor_id": doctor_id})


# ---------- Admin: students ----------

def list_students():
    return _get("/admin/students")


def add_student(student_id, name, email, department):
    return _post("/admin/students", {"student_id": student_id, "name": name, "email": email, "department": department})


def update_student(student_id, name, email, department):
    return _put(f"/admin/students/{student_id}", {"name": name, "email": email, "department": department})


def delete_student(student_id):
    return _delete(f"/admin/students/{student_id}")


# ---------- Admin: instructors / doctors ----------

def list_instructors():
    return _get("/admin/instructors")


def list_doctors():
    return _get("/admin/doctors")


def add_staff(role, name, email, password, specialization=None):
    return _post("/admin/staff", {
        "name": name, "email": email, "password": password, "specialization": specialization,
    }, params={"role": role})


def update_staff(role, email, name, specialization=None):
    return _put(f"/admin/staff/{email}", {"name": name, "specialization": specialization}, params={"role": role})


def delete_staff(role, email):
    return _delete(f"/admin/staff/{email}", params={"role": role})


# ---------- Admin: combined course view ----------

def combined_course_view(course_id):
    return _get(f"/admin/courses/{course_id}/combined")
