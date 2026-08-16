from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    """
    One row per instructor / doctor / admin account.
    `role` is set automatically at registration time from the email
    domain (see auth/authentication.py) and is what login.py and app.py
    use to route each person to the right dashboard.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False, index=True)

    password_hash = Column(String, nullable=False)

    role = Column(String, nullable=False)  # "instructor" | "doctor" | "admin"

    specialization = Column(String, nullable=True)  # only meaningful for role="doctor"

    created_at = Column(DateTime, default=datetime.utcnow)


class Student(Base):
    """
    Historical/bulk dataset table — this is what import_csv.py loads the
    Cleaned_Students_Performance.csv into for model training. It is NOT
    the live student directory used by the app's course/enrollment
    screens; that's StudentProfile below. Kept separate on purpose so
    importing a fresh CSV never touches live course data.
    """

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(String, unique=True, nullable=False)

    attendance = Column(Float)

    study_hours = Column(Float)

    extracurricular = Column(String)

    internet_access = Column(String)

    sleep_hours = Column(Float)

    stress_level = Column(Float)


class Course(Base):
    """A course section created by an instructor (Add Course page)."""

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)

    course_name = Column(String, nullable=False)   # e.g. "CSE299"
    section = Column(String, nullable=False)
    semester = Column(String, nullable=False)

    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan",
    )


class StudentProfile(Base):
    """
    The live student directory: one row per real student, identified by
    their university student ID. Created on the fly the first time an
    instructor enrolls that student in a course (see manage_course.py)
    or the first time a doctor assesses them (see new_student_assessment.py).
    """

    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    department = Column(String)

    enrollments = relationship("Enrollment", back_populates="student")
    assessments = relationship("StudentAssessment", back_populates="student")


class Enrollment(Base):
    """
    One row per (course, student) — the instructor's academic record
    for that student in that course: attendance %, quiz marks, mid marks.
    """

    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)

    attendance = Column(Float)     # percentage, e.g. 92.0
    quiz_marks = Column(Float)
    mid_marks = Column(Float)

    course = relationship("Course", back_populates="enrollments")
    student = relationship("StudentProfile", back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint("course_id", "student_id", name="uq_course_student"),
    )


class StudentAssessment(Base):
    """
    One row per doctor visit/assessment. A student can be assessed more
    than once over time, so this is a history log, not a single record
    per student — assessment_history.py lists these, edit_student_assessment.py
    edits/deletes the most recent one for a given student.
    """

    __tablename__ = "student_assessments"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    sleep_hours = Column(Float)
    extracurricular_hours = Column(Float)
    internet_usage_hours = Column(Float)
    stress_level = Column(Integer)  # 1-10

    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentProfile", back_populates="assessments")
    doctor = relationship("User")