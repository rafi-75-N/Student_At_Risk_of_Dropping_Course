import pandas as pd

from api.db import SessionLocal
from api.models import Student

db = SessionLocal()

df = pd.read_csv("Cleaned_Students_Performance.csv")

print(f"Found {len(df)} students.")

for _, row in df.iterrows():

    student = Student(

        student_id=row["Student_ID"],

        attendance=row["Attendance (%)"],

        study_hours=row["Study_Hours_per_Week"],

        extracurricular=row["Extracurricular_Activities"],

        internet_access=row["Internet_Access_at_Home"],

        sleep_hours=row["Sleep_Hours_per_Night"],

        stress_level=row["Stress_Level (1-10)"]

    )

    db.add(student)

db.commit()

db.close()

print("Import successful!")