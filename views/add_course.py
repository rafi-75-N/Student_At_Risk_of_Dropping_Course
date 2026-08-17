import streamlit as st

from utils.ui import load_css
from utils import api_client


def show_add_course():

    load_css()

    st.title("Add Course")

    course_name = st.text_input("Course Name")

    section = st.text_input("Section")

    semester = st.text_input("Semester")

    if st.button("Create Course"):

        if not course_name or not section or not semester:

            st.error("Please fill in all fields.")

        else:

            user = st.session_state.get("user") or {}

            try:
                result = api_client.create_course(course_name, section, semester, user.get("id"))

                if result["success"]:
                    st.success(result["message"])
                else:
                    st.error(result["message"])

            except Exception:
                st.error("Couldn't reach the server. Is the API running?")

    if st.button("← Back"):

        st.session_state.page = "instructor_dashboard"

        st.rerun()