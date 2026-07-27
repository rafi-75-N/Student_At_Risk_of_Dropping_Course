import streamlit as st

from utils.ui import load_css


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

            st.success(
                "Assessment saved successfully!"
            )

    with col2:

        if st.button(
            "Back",
            use_container_width=True
        ):

            st.session_state.page = "doctor_dashboard"

            st.rerun()