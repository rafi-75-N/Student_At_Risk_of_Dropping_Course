import streamlit as st

from utils.ui import load_css
from utils import api_client


def show_edit_student_assessment():

    load_css()

    st.title("Edit Student Assessment")

    st.markdown("---")

    student_id = st.text_input("Enter Student ID", key="esa_search_id")

    if st.button("Search", use_container_width=True):

        try:
            result = api_client.search_latest_assessment(student_id)

            if result["found"]:
                st.session_state.esa_loaded = result["assessment"]
                st.success("Assessment found.")
            else:
                st.session_state.esa_loaded = None
                st.warning("No assessment found for that Student ID.")

        except Exception:
            st.error("Couldn't reach the server. Is the API running?")

    loaded = st.session_state.get("esa_loaded")

    st.markdown("### Student Information")

    if loaded:

        student_name = st.text_input("Student Name", value=loaded["student_name"])

        attendance = st.number_input(
            "Attendance (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(loaded["attendance"] or 0),
            step=1.0
        )

        study_hours = st.number_input(
            "Study Hours (per week)",
            min_value=0.0,
            value=float(loaded["study_hours"] or 0),
            step=1.0
        )

        sleep_hours = st.number_input(
            "Sleep Hours (per day)",
            min_value=0.0,
            max_value=24.0,
            value=float(loaded["sleep_hours"] or 0),
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

            if st.button("Save Changes", use_container_width=True):

                try:
                    result = api_client.update_assessment(
                        loaded["id"], student_name, attendance, study_hours, sleep_hours, stress_level,
                    )

                    if result["success"]:
                        st.success(result["message"])
                    else:
                        st.error(result["message"])

                except Exception:
                    st.error("Couldn't reach the server. Is the API running?")

        with col2:

            if st.button("Delete Assessment", use_container_width=True):

                try:
                    result = api_client.delete_assessment(loaded["id"])

                    st.session_state.esa_loaded = None

                    if result["success"]:
                        st.warning(result["message"])
                    else:
                        st.error(result["message"])

                    st.rerun()

                except Exception:
                    st.error("Couldn't reach the server. Is the API running?")

        with col3:

            if st.button("Back", use_container_width=True):

                st.session_state.esa_loaded = None

                st.session_state.page = "doctor_dashboard"

                st.rerun()

    else:

        st.info("Search for a Student ID above to load their most recent assessment.")

        if st.button("Back", use_container_width=True, key="esa_back_no_result"):

            st.session_state.page = "doctor_dashboard"

            st.rerun()
