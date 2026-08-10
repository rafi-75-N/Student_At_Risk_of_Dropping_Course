import streamlit as st

from utils.ui import load_css
from api.db import SessionLocal
from api.models import StudentAssessment, StudentProfile


def show_assessment_history():

    load_css()

    st.title("Assessment History")

    st.markdown("---")

    user = st.session_state.get("user") or {}

    db = SessionLocal()

    try:
        assessments = (
            db.query(StudentAssessment)
            .join(StudentProfile)
            .filter(StudentAssessment.doctor_id == user.get("id"))
            .order_by(StudentAssessment.created_at.desc())
            .all()
        )

        if not assessments:

            st.info("No assessments recorded yet.")

        else:

            rows = [
                {
                    "Student ID": a.student.student_id,
                    "Student Name": a.student.name,
                    "Sleep Hours": a.sleep_hours,
                    "Internet Usage": a.internet_usage_hours,
                    "Stress Level": a.stress_level,
                    "Date": a.created_at.strftime("%Y-%m-%d %H:%M"),
                }
                for a in assessments
            ]

            st.dataframe(
                rows,
                use_container_width=True
            )

    finally:
        db.close()

    st.markdown("")

    if st.button(
        "Back",
        use_container_width=True
    ):

        st.session_state.page = "doctor_dashboard"

        st.rerun()