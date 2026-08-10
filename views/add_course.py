import streamlit as st

from utils.ui import load_css
from api.db import SessionLocal
from api.models import Course


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

            db = SessionLocal()

            try:
                course = Course(
                    course_name=course_name,
                    section=section,
                    semester=semester,
                    instructor_id=user.get("id"),
                )

                db.add(course)
                db.commit()

                st.success(f"Course '{course_name}' created successfully!")

            finally:
                db.close()

    if st.button("← Back"):

        st.session_state.page = "instructor_dashboard"

        st.rerun()