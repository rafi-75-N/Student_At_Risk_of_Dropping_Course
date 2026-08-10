import streamlit as st

from utils.ui import load_css
from api.db import SessionLocal
from api.models import StudentProfile, StudentAssessment


def show_edit_student_assessment():

    load_css()

    st.title("Edit Student Assessment")

    st.markdown("---")

    student_id = st.text_input(
        "Enter Student ID",
        key="esa_search_id"
    )

    if st.button(
        "Search",
        use_container_width=True
    ):

        db = SessionLocal()

        try:
            student = (
                db.query(StudentProfile)
                .filter(StudentProfile.student_id == student_id)
                .first()
            )

            assessment = None

            if student:

                assessment = (
                    db.query(StudentAssessment)
                    .filter(StudentAssessment.student_id == student.id)
                    .order_by(StudentAssessment.created_at.desc())
                    .first()
                )

            if assessment:

                st.session_state.esa_loaded = {
                    "assessment_id": assessment.id,
                    "student_name": student.name,
                    "sleep_hours": assessment.sleep_hours,
                    "extracurricular": assessment.extracurricular_hours,
                    "internet_usage": assessment.internet_usage_hours,
                    "stress_level": assessment.stress_level,
                }

                st.success("Assessment found.")

            else:

                st.session_state.esa_loaded = None

                st.warning("No assessment found for that Student ID.")

        finally:
            db.close()

    loaded = st.session_state.get("esa_loaded")

    st.markdown("### Student Information")

    if loaded:

        student_name = st.text_input(
            "Student Name",
            value=loaded["student_name"]
        )

        sleep_hours = st.number_input(
            "Sleep Hours (per day)",
            min_value=0.0,
            max_value=24.0,
            value=float(loaded["sleep_hours"] or 0),
            step=0.5
        )

        extracurricular = st.number_input(
            "Extracurricular Activity Hours (per week)",
            min_value=0.0,
            value=float(loaded["extracurricular"] or 0),
            step=1.0
        )

        internet_usage = st.number_input(
            "Internet Usage (hours per day)",
            min_value=0.0,
            max_value=24.0,
            value=float(loaded["internet_usage"] or 0),
            step=0.5
        )

        stress_level = st.slider(
            "Stress Level Score",
            min_value=1,
            max_value=10,
            value=int(loaded["stress_level"] or 5)
        )

        st.markdown("")

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "Save Changes",
                use_container_width=True
            ):

                db = SessionLocal()

                try:
                    assessment = (
                        db.query(StudentAssessment)
                        .filter(StudentAssessment.id == loaded["assessment_id"])
                        .first()
                    )

                    if assessment:

                        assessment.sleep_hours = sleep_hours
                        assessment.extracurricular_hours = extracurricular
                        assessment.internet_usage_hours = internet_usage
                        assessment.stress_level = stress_level
                        assessment.student.name = student_name

                        db.commit()

                        st.success("Changes Saved Successfully!")

                finally:
                    db.close()

        with col2:

            if st.button(
                "Delete Assessment",
                use_container_width=True
            ):

                db = SessionLocal()

                try:
                    db.query(StudentAssessment).filter(
                        StudentAssessment.id == loaded["assessment_id"]
                    ).delete()

                    db.commit()

                    st.session_state.esa_loaded = None

                    st.warning("Assessment Deleted!")

                    st.rerun()

                finally:
                    db.close()

        with col3:

            if st.button(
                "Back",
                use_container_width=True
            ):

                st.session_state.esa_loaded = None

                st.session_state.page = "doctor_dashboard"

                st.rerun()

    else:

        st.info("Search for a Student ID above to load their most recent assessment.")

        if st.button(
            "Back",
            use_container_width=True,
            key="esa_back_no_result"
        ):

            st.session_state.page = "doctor_dashboard"

            st.rerun()