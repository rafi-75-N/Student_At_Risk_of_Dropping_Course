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

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "instructor" | "doctor" | "admin"
    specialization = Column(String, nullable=True)  # doctors only
    created_at = Column(DateTime, default=datetime.utcnow)


class Student(Base):
    """
    Historical/bulk dataset table — what a CSV import script would load
    into for model training. Not the live student directory (that's
    StudentProfile below).
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

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
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
    """The live student directory — one row per real student."""

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
    The instructor's academic record for a student in a course.
    Matches the 5 instructor-owned columns from Students_Performance_Dataset.csv.
    Attendance lives on StudentAssessment now (doctor-owned).
    """

    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)

    midterm_score = Column(Float)
    assignments_avg = Column(Float)
    quizzes_avg = Column(Float)
    participation_score = Column(Float)
    projects_score = Column(Float)

    course = relationship("Course", back_populates="enrollments")
    student = relationship("StudentProfile", back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint("course_id", "student_id", name="uq_course_student"),
    )


class StudentAssessment(Base):
    """
    A doctor's assessment of a student — one row per visit (history log).
    Matches the 4 doctor-owned columns from Students_Performance_Dataset.csv.
    """

    __tablename__ = "student_assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    attendance = Column(Float)       # percentage, e.g. 92.0
    study_hours = Column(Float)      # per week
    sleep_hours = Column(Float)      # per night
    stress_level = Column(Integer)   # 1-10

    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("StudentProfile", back_populates="assessments")
    doctor = relationship("User")
