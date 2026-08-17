from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


# ---------- Auth ----------

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    confirm: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str
    specialization: Optional[str] = None


class AuthResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    user: Optional[UserOut] = None


class ActionResponse(BaseModel):
    success: bool
    message: str


# ---------- Courses ----------

class CourseCreate(BaseModel):
    course_name: str
    section: str
    semester: str
    instructor_id: int


class CourseOut(BaseModel):
    id: int
    course_name: str
    section: str
    semester: str
    student_count: int = 0


# ---------- Enrollments ----------

class EnrollmentUpsert(BaseModel):
    course_id: int
    student_id: str
    student_name: str
    student_email: Optional[str] = None
    midterm_score: Optional[float] = None
    assignments_avg: Optional[float] = None
    quizzes_avg: Optional[float] = None
    participation_score: Optional[float] = None
    projects_score: Optional[float] = None


class EnrollmentOut(BaseModel):
    student_id: str
    name: str
    midterm_score: Optional[float] = None
    assignments_avg: Optional[float] = None
    quizzes_avg: Optional[float] = None
    participation_score: Optional[float] = None
    projects_score: Optional[float] = None


# ---------- Assessments ----------

class AssessmentCreate(BaseModel):
    student_id: str
    student_name: str
    doctor_id: int
    attendance: Optional[float] = None
    study_hours: Optional[float] = None
    sleep_hours: Optional[float] = None
    stress_level: Optional[int] = None


class AssessmentUpdate(BaseModel):
    student_name: Optional[str] = None
    attendance: Optional[float] = None
    study_hours: Optional[float] = None
    sleep_hours: Optional[float] = None
    stress_level: Optional[int] = None


class AssessmentOut(BaseModel):
    id: int
    student_id: str
    student_name: str
    attendance: Optional[float] = None
    study_hours: Optional[float] = None
    sleep_hours: Optional[float] = None
    stress_level: Optional[int] = None
    created_at: datetime


class AssessmentSearchResult(BaseModel):
    found: bool
    assessment: Optional[AssessmentOut] = None


# ---------- Admin: students ----------

class StudentCreate(BaseModel):
    student_id: str
    name: str
    email: Optional[str] = None
    department: Optional[str] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None


class StudentOut(BaseModel):
    student_id: str
    name: str
    email: Optional[str] = None
    department: Optional[str] = None


# ---------- Admin: instructors / doctors ----------

class StaffCreate(BaseModel):
    name: str
    email: str
    password: str
    specialization: Optional[str] = None  # doctors only


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None


class StaffOut(BaseModel):
    name: str
    email: str
    specialization: Optional[str] = None
    count: int = 0  # courses for instructors, assessments for doctors


# ---------- Admin: combined course view ----------

class CombinedStudentRow(BaseModel):
    student_id: str
    name: str
    midterm_score: Optional[float] = None
    assignments_avg: Optional[float] = None
    quizzes_avg: Optional[float] = None
    participation_score: Optional[float] = None
    projects_score: Optional[float] = None
    attendance: Optional[float] = None
    study_hours: Optional[float] = None
    sleep_hours: Optional[float] = None
    stress_level: Optional[int] = None
    # Computed by api/risk_engine.py — None if instructor or doctor data is incomplete
    instructor_marks: Optional[float] = None
    doctor_marks: Optional[float] = None
    performance_score: Optional[float] = None
    grade: Optional[str] = None
    risk_level: Optional[str] = None
    # From the trained XGBoost model (api/ml_model.py) — None until train_model.py has been run
    doctor_effect: Optional[float] = None
