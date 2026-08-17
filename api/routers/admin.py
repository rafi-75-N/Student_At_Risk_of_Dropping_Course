from typing import List

from fastapi import APIRouter

from ..db import SessionLocal
from ..models import StudentProfile, Enrollment, StudentAssessment, User, Course
from ..security import get_role_from_email, hash_password
from .. import risk_engine
from .. import ml_model
from ..schemas import (
    StudentCreate,
    StudentUpdate,
    StudentOut,
    StaffCreate,
    StaffUpdate,
    StaffOut,
    ActionResponse,
    CombinedStudentRow,
)

router = APIRouter(prefix="/admin", tags=["admin"])


# ---------- Students ----------

@router.get("/students", response_model=List[StudentOut])
def list_students():

    db = SessionLocal()

    try:
        students = db.query(StudentProfile).order_by(StudentProfile.student_id).all()

        return [
            StudentOut(
                student_id=s.student_id,
                name=s.name,
                email=s.email,
                department=s.department,
            )
            for s in students
        ]

    finally:
        db.close()


@router.post("/students", response_model=ActionResponse)
def add_student(payload: StudentCreate):

    db = SessionLocal()

    try:
        existing = (
            db.query(StudentProfile)
            .filter(StudentProfile.student_id == payload.student_id)
            .first()
        )

        if existing:
            return ActionResponse(success=False, message="A student with this ID already exists.")

        db.add(StudentProfile(
            student_id=payload.student_id,
            name=payload.name,
            email=payload.email,
            department=payload.department,
        ))

        db.commit()

        return ActionResponse(success=True, message="Student Added Successfully!")

    finally:
        db.close()


@router.put("/students/{student_id}", response_model=ActionResponse)
def update_student(student_id: str, payload: StudentUpdate):

    db = SessionLocal()

    try:
        student = (
            db.query(StudentProfile)
            .filter(StudentProfile.student_id == student_id)
            .first()
        )

        if not student:
            return ActionResponse(success=False, message="No student found with that ID.")

        if payload.name:
            student.name = payload.name

        if payload.email:
            student.email = payload.email

        student.department = payload.department

        db.commit()

        return ActionResponse(success=True, message="Student Information Updated!")

    finally:
        db.close()


@router.delete("/students/{student_id}", response_model=ActionResponse)
def delete_student(student_id: str):

    db = SessionLocal()

    try:
        student = (
            db.query(StudentProfile)
            .filter(StudentProfile.student_id == student_id)
            .first()
        )

        if not student:
            return ActionResponse(success=False, message="No student found with that ID.")

        has_enrollments = (
            db.query(Enrollment).filter(Enrollment.student_id == student.id).first() is not None
        )

        has_assessments = (
            db.query(StudentAssessment).filter(StudentAssessment.student_id == student.id).first() is not None
        )

        if has_enrollments or has_assessments:
            return ActionResponse(
                success=False,
                message="Can't delete: this student has course or assessment records tied to them. Remove those first.",
            )

        db.delete(student)
        db.commit()

        return ActionResponse(success=True, message="Student Deleted!")

    finally:
        db.close()


# ---------- Instructors / Doctors (shared logic, filtered by role) ----------

def _staff_out(db, user, role):

    if role == "instructor":
        count = db.query(Course).filter(Course.instructor_id == user.id).count()
    else:
        count = db.query(StudentAssessment).filter(StudentAssessment.doctor_id == user.id).count()

    return StaffOut(
        name=user.name,
        email=user.email,
        specialization=user.specialization,
        count=count,
    )


@router.get("/instructors", response_model=List[StaffOut])
def list_instructors():

    db = SessionLocal()

    try:
        instructors = db.query(User).filter(User.role == "instructor").order_by(User.name).all()

        return [_staff_out(db, i, "instructor") for i in instructors]

    finally:
        db.close()


@router.get("/doctors", response_model=List[StaffOut])
def list_doctors():

    db = SessionLocal()

    try:
        doctors = db.query(User).filter(User.role == "doctor").order_by(User.name).all()

        return [_staff_out(db, d, "doctor") for d in doctors]

    finally:
        db.close()


@router.post("/staff", response_model=ActionResponse)
def add_staff(payload: StaffCreate, role: str):
    """role must be 'instructor' or 'doctor'."""

    if get_role_from_email(payload.email) != role:
        domain = "@northsouth.edu" if role == "instructor" else "@docnorthsouth.edu"
        return ActionResponse(success=False, message=f"Email must end in {domain} for a {role} account.")

    db = SessionLocal()

    try:
        existing = db.query(User).filter(User.email.ilike(payload.email)).first()

        if existing:
            return ActionResponse(success=False, message="An account with this email already exists.")

        db.add(User(
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password),
            role=role,
            specialization=payload.specialization if role == "doctor" else None,
        ))

        db.commit()

        return ActionResponse(
            success=True,
            message=f"{role.title()} added. Share the temporary password with them directly so they can log in.",
        )

    finally:
        db.close()


@router.put("/staff/{email}", response_model=ActionResponse)
def update_staff(email: str, payload: StaffUpdate, role: str):

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email.ilike(email), User.role == role).first()

        if not user:
            return ActionResponse(success=False, message=f"No {role} found with that email.")

        if payload.name:
            user.name = payload.name

        if role == "doctor":
            user.specialization = payload.specialization

        db.commit()

        return ActionResponse(success=True, message=f"{role.title()} Updated Successfully!")

    finally:
        db.close()


@router.delete("/staff/{email}", response_model=ActionResponse)
def delete_staff(email: str, role: str):

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email.ilike(email), User.role == role).first()

        if not user:
            return ActionResponse(success=False, message=f"No {role} found with that email.")

        if role == "instructor":
            has_records = db.query(Course).filter(Course.instructor_id == user.id).first() is not None
            noun = "courses"
        else:
            has_records = db.query(StudentAssessment).filter(StudentAssessment.doctor_id == user.id).first() is not None
            noun = "assessments"

        if has_records:
            return ActionResponse(
                success=False,
                message=f"Can't delete: this {role} has {noun} on record. Remove those first.",
            )

        db.delete(user)
        db.commit()

        return ActionResponse(success=True, message=f"{role.title()} Deleted!")

    finally:
        db.close()


# ---------- Combined course view ----------

@router.get("/courses/{course_id}/combined", response_model=List[CombinedStudentRow])
def combined_course_view(course_id: int):
    """
    Merges the instructor's Enrollment record with each student's most
    recent doctor Assessment — the 'combination of the two people' view.
    """

    db = SessionLocal()

    try:
        enrollments = (
            db.query(Enrollment)
            .join(StudentProfile)
            .filter(Enrollment.course_id == course_id)
            .all()
        )

        rows = []

        for e in enrollments:

            latest_assessment = (
                db.query(StudentAssessment)
                .filter(StudentAssessment.student_id == e.student_id)
                .order_by(StudentAssessment.created_at.desc())
                .first()
            )

            attendance = latest_assessment.attendance if latest_assessment else None
            study_hours = latest_assessment.study_hours if latest_assessment else None
            sleep_hours = latest_assessment.sleep_hours if latest_assessment else None
            stress_level = latest_assessment.stress_level if latest_assessment else None

            evaluation = risk_engine.evaluate_student(
                e.midterm_score, e.assignments_avg, e.quizzes_avg,
                e.participation_score, e.projects_score,
                attendance, study_hours, stress_level, sleep_hours,
            )

            instructor_marks = doctor_marks = None
            performance_score = grade = risk_level = doctor_effect = None

            if evaluation:

                instructor_marks = evaluation["instructor_marks"]
                doctor_marks = evaluation["doctor_marks"]

                # Prefer the trained XGBoost model when it's available;
                # fall back to the plain formula (identical weights, no
                # doctor-effect counterfactual) if train_model.py hasn't
                # been run yet.
                model_result = ml_model.predict(
                    e.midterm_score, e.assignments_avg, e.quizzes_avg,
                    e.participation_score, e.projects_score,
                    attendance, study_hours, stress_level, sleep_hours,
                )

                if model_result:
                    performance_score, doctor_effect = model_result
                else:
                    performance_score = evaluation["performance_score"]

                grade = risk_engine.grade_from_score(performance_score)
                risk_level = risk_engine.risk_from_score(performance_score)

            rows.append(CombinedStudentRow(
                student_id=e.student.student_id,
                name=e.student.name,
                midterm_score=e.midterm_score,
                assignments_avg=e.assignments_avg,
                quizzes_avg=e.quizzes_avg,
                participation_score=e.participation_score,
                projects_score=e.projects_score,
                attendance=attendance,
                study_hours=study_hours,
                sleep_hours=sleep_hours,
                stress_level=stress_level,
                instructor_marks=instructor_marks,
                doctor_marks=doctor_marks,
                performance_score=performance_score,
                grade=grade,
                risk_level=risk_level,
                doctor_effect=doctor_effect,
            ))

        return rows

    finally:
        db.close()
