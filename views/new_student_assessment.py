import streamlit as st

from utils.ui import load_css
from utils import api_client


def show_new_student_assessment():

    load_css()

    st.title("New Student Assessment")

    st.markdown("---")

    student_id = st.text_input("Student ID")

    student_name = st.text_input("Student Name")

    attendance = st.number_input(
        "Attendance (%)",
        min_value=0.0,
        max_value=100.0,
        step=1.0
    )

    study_hours = st.number_input(
        "Study Hours (per week)",
        min_value=0.0,
        step=1.0
    )

    sleep_hours = st.number_input(
        "Sleep Hours (per day)",
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

        if st.button("Save Assessment", use_container_width=True):

            if not student_id or not student_name:

                st.error("Student ID and Name are required.")

            else:

                user = st.session_state.get("user") or {}

                try:
                    result = api_client.create_assessment(
                        student_id, student_name, user.get("id"),
                        attendance, study_hours, sleep_hours, stress_level,
                    )

                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(result["message"])

                except Exception:
                    st.error("Couldn't reach the server. Is the API running?")

    with col2:

        if st.button("Back", use_container_width=True):

            st.session_state.page = "doctor_dashboard"

            st.rerun()
