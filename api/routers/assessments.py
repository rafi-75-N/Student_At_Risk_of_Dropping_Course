from typing import List

from fastapi import APIRouter

from ..db import SessionLocal
from ..models import StudentProfile, StudentAssessment
from ..schemas import (
    AssessmentCreate,
    AssessmentUpdate,
    AssessmentOut,
    AssessmentSearchResult,
    ActionResponse,
)

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post("", response_model=ActionResponse)
def create_assessment(payload: AssessmentCreate):
    """Creates the StudentProfile if needed, then logs a new assessment row."""

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
            )

            db.add(student)
            db.flush()

        else:

            student.name = payload.student_name

        assessment = StudentAssessment(
            student_id=student.id,
            doctor_id=payload.doctor_id,
            attendance=payload.attendance,
            study_hours=payload.study_hours,
            sleep_hours=payload.sleep_hours,
            stress_level=payload.stress_level,
        )

        db.add(assessment)
        db.commit()

        return ActionResponse(success=True, message="Assessment saved successfully!")

    finally:
        db.close()


@router.get("/search", response_model=AssessmentSearchResult)
def search_latest_assessment(student_id: str):
    """Finds a student's most recent assessment, for the Edit screen."""

    db = SessionLocal()

    try:
        student = (
            db.query(StudentProfile)
            .filter(StudentProfile.student_id == student_id)
            .first()
        )

        if not student:
            return AssessmentSearchResult(found=False)

        assessment = (
            db.query(StudentAssessment)
            .filter(StudentAssessment.student_id == student.id)
            .order_by(StudentAssessment.created_at.desc())
            .first()
        )

        if not assessment:
            return AssessmentSearchResult(found=False)

        return AssessmentSearchResult(
            found=True,
            assessment=AssessmentOut(
                id=assessment.id,
                student_id=student.student_id,
                student_name=student.name,
                attendance=assessment.attendance,
                study_hours=assessment.study_hours,
                sleep_hours=assessment.sleep_hours,
                stress_level=assessment.stress_level,
                created_at=assessment.created_at,
            ),
        )

    finally:
        db.close()


@router.put("/{assessment_id}", response_model=ActionResponse)
def update_assessment(assessment_id: int, payload: AssessmentUpdate):

    db = SessionLocal()

    try:
        assessment = (
            db.query(StudentAssessment)
            .filter(StudentAssessment.id == assessment_id)
            .first()
        )

        if not assessment:
            return ActionResponse(success=False, message="Assessment not found.")

        assessment.attendance = payload.attendance
        assessment.study_hours = payload.study_hours
        assessment.sleep_hours = payload.sleep_hours
        assessment.stress_level = payload.stress_level

        if payload.student_name:
            assessment.student.name = payload.student_name

        db.commit()

        return ActionResponse(success=True, message="Changes Saved Successfully!")

    finally:
        db.close()


@router.delete("/{assessment_id}", response_model=ActionResponse)
def delete_assessment(assessment_id: int):

    db = SessionLocal()

    try:
        db.query(StudentAssessment).filter(
            StudentAssessment.id == assessment_id
        ).delete()

        db.commit()

        return ActionResponse(success=True, message="Assessment Deleted!")

    finally:
        db.close()


@router.get("/history", response_model=List[AssessmentOut])
def assessment_history(doctor_id: int):

    db = SessionLocal()

    try:
        assessments = (
            db.query(StudentAssessment)
            .join(StudentProfile)
            .filter(StudentAssessment.doctor_id == doctor_id)
            .order_by(StudentAssessment.created_at.desc())
            .all()
        )

        return [
            AssessmentOut(
                id=a.id,
                student_id=a.student.student_id,
                student_name=a.student.name,
                attendance=a.attendance,
                study_hours=a.study_hours,
                sleep_hours=a.sleep_hours,
                stress_level=a.stress_level,
                created_at=a.created_at,
            )
            for a in assessments
        ]

    finally:
        db.close()
