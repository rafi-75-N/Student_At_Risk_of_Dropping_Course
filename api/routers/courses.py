from typing import List, Optional

from fastapi import APIRouter

from ..db import SessionLocal
from ..models import Course, StudentProfile, Enrollment
from ..schemas import (
    CourseCreate,
    CourseOut,
    ActionResponse,
    EnrollmentUpsert,
    EnrollmentOut,
)

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("", response_model=ActionResponse)
def create_course(payload: CourseCreate):

    db = SessionLocal()

    try:
        course = Course(
            course_name=payload.course_name,
            section=payload.section,
            semester=payload.semester,
            instructor_id=payload.instructor_id,
        )

        db.add(course)
        db.commit()

        return ActionResponse(success=True, message=f"Course '{payload.course_name}' created successfully!")

    finally:
        db.close()


@router.get("", response_model=List[CourseOut])
def list_courses(instructor_id: Optional[int] = None):
    """List all courses, or only one instructor's if instructor_id is given."""

    db = SessionLocal()

    try:
        query = db.query(Course)

        if instructor_id is not None:
            query = query.filter(Course.instructor_id == instructor_id)

        courses = query.order_by(Course.course_name).all()

        return [
            CourseOut(
                id=c.id,
                course_name=c.course_name,
                section=c.section,
                semester=c.semester,
                student_count=len(c.enrollments),
            )
            for c in courses
        ]

    finally:
        db.close()


@router.get("/{course_id}/enrollments", response_model=List[EnrollmentOut])
def list_enrollments(course_id: int):

    db = SessionLocal()

    try:
        enrollments = (
            db.query(Enrollment)
            .join(StudentProfile)
            .filter(Enrollment.course_id == course_id)
            .all()
        )

        return [
            EnrollmentOut(
                student_id=e.student.student_id,
                name=e.student.name,
                midterm_score=e.midterm_score,
                assignments_avg=e.assignments_avg,
                quizzes_avg=e.quizzes_avg,
                participation_score=e.participation_score,
                projects_score=e.projects_score,
            )
            for e in enrollments
        ]

    finally:
        db.close()


@router.post("/enrollments", response_model=ActionResponse)
def upsert_enrollment(payload: EnrollmentUpsert):
    """Creates the StudentProfile if needed, then creates/updates the enrollment record."""

    db = SessionLocal()

    try:
        student = (
            db.query(StudentProfile)
            .filter(StudentProfile.student_id == payload.student_id)
            .first()
        )

        if not student:

            student = StudentProfile(
                student_id=payload.student_id,
                name=payload.student_name,
                email=payload.student_email,
            )

            db.add(student)
            db.flush()

        else:

            student.name = payload.student_name

            if payload.student_email:
                student.email = payload.student_email

        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.course_id == payload.course_id,
                Enrollment.student_id == student.id,
            )
            .first()
        )

        if not enrollment:

            enrollment = Enrollment(
                course_id=payload.course_id,
                student_id=student.id,
            )

            db.add(enrollment)

        enrollment.midterm_score = payload.midterm_score
        enrollment.assignments_avg = payload.assignments_avg
        enrollment.quizzes_avg = payload.quizzes_avg
        enrollment.participation_score = payload.participation_score
        enrollment.projects_score = payload.projects_score

        db.commit()

        return ActionResponse(success=True, message=f"Record saved for {payload.student_name}.")

    finally:
        db.close()


@router.delete("/{course_id}/enrollments/{student_id}", response_model=ActionResponse)
def remove_enrollment(course_id: int, student_id: str):

    db = SessionLocal()

    try:
        student = (
            db.query(StudentProfile)
            .filter(StudentProfile.student_id == student_id)
            .first()
        )

        if not student:
            return ActionResponse(success=False, message="No such student found.")

        db.query(Enrollment).filter(
            Enrollment.course_id == course_id,
            Enrollment.student_id == student.id,
        ).delete()

        db.commit()

        return ActionResponse(success=True, message=f"Removed {student_id} from this course.")

    finally:
        db.close()
