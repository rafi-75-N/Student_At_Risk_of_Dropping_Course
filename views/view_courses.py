import streamlit as st

from utils.ui import load_css
from utils import api_client


def show_view_courses():

    load_css()

    st.title("My Courses")

    user = st.session_state.get("user") or {}

    try:
        courses = api_client.list_courses(instructor_id=user.get("id"))

    except Exception:
        st.error("Couldn't reach the server. Is the API running?")
        courses = []

    if not courses:

        st.info("No courses have been added yet.")

    else:

        rows = [
            {
                "Course": c["course_name"],
                "Section": c["section"],
                "Semester": c["semester"],
                "Students Enrolled": c["student_count"],
            }
            for c in courses
        ]

        st.dataframe(rows, use_container_width=True)

    if st.button("← Back"):
        st.session_state.page = "instructor_dashboard"
        st.rerun()
