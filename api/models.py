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

    created_at = Column(DateTime, default=datetime.utcnow)


class Student(Base):

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