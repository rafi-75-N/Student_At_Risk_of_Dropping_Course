import streamlit as st

from utils.ui import load_css
from utils import api_client


def show_assessment_history():

    load_css()

    st.title("Assessment History")

    st.markdown("---")

    user = st.session_state.get("user") or {}

    try:
        assessments = api_client.assessment_history(user.get("id"))

    except Exception:
        st.error("Couldn't reach the server. Is the API running?")
        assessments = []

    if not assessments:

        st.info("No assessments recorded yet.")

    else:

        rows = [
            {
                "Student ID": a["student_id"],
                "Student Name": a["student_name"],
                "Attendance (%)": a["attendance"],
                "Study Hours": a["study_hours"],
                "Sleep Hours": a["sleep_hours"],
                "Stress Level": a["stress_level"],
                "Date": a["created_at"][:16].replace("T", " "),
            }
            for a in assessments
        ]

        st.dataframe(rows, use_container_width=True)

    st.markdown("")

    if st.button("Back", use_container_width=True):

        st.session_state.page = "doctor_dashboard"

        st.rerun()
