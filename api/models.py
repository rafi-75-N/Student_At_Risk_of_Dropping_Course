from sqlalchemy import Column, Integer, Float, String

from .db import Base


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