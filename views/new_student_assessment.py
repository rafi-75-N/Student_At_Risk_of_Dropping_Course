import streamlit as st

from utils.ui import load_css
from api.db import SessionLocal
from api.models import StudentProfile, StudentAssessment


def show_new_student_assessment():

    load_css()

    st.title("New Student Assessment")

    st.markdown("---")

    student_id = st.text_input(
        "Student ID"
    )

    student_name = st.text_input(
        "Student Name"
    )

    sleep_hours = st.number_input(
        "Sleep Hours (per day)",
        min_value=0.0,
        max_value=24.0,
        step=0.5
    )

    extracurricular = st.number_input(
        "Extracurricular Activity Hours (per week)",
        min_value=0.0,
        step=1.0
    )

    internet_usage = st.number_input(
        "Internet Usage (hours per day)",
        min_value=0.0,
        max_value=24.0,
        step=0.5
    )

    stress_level = st.slider(
        "Stress Level Score",
        min_value=1,
        max_value=10,
        value=5
    )

    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Save Assessment",
            use_container_width=True
        ):

            if not student_id or not student_name:

                st.error("Student ID and Name are required.")

            else:

                user = st.session_state.get("user") or {}

                db = SessionLocal()

                try:
                    student = (
                        db.query(StudentProfile)
                        .filter(StudentProfile.student_id == student_id)
                        .first()
                    )

                    if not student:

                        student = StudentProfile(
                            student_id=student_id,
                            name=student_name,
                        )

                        db.add(student)
                        db.flush()  # assigns student.id before we use it below

                    else:

                        student.name = student_name

                    assessment = StudentAssessment(
                        student_id=student.id,
                        doctor_id=user.get("id"),
                        sleep_hours=sleep_hours,
                        extracurricular_hours=extracurricular,
                        internet_usage_hours=internet_usage,
                        stress_level=stress_level,
                    )

                    db.add(assessment)
                    db.commit()

                    st.success(
                        "Assessment saved successfully!"
                    )

                finally:
                    db.close()

    with col2:

        if st.button(
            "Back",
            use_container_width=True
        ):

            st.session_state.page = "doctor_dashboard"

            st.rerun()