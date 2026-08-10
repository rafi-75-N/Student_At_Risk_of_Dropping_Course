import streamlit as st

from utils.ui import load_css
from api.db import SessionLocal
from api.models import Course


def show_view_courses():

    load_css()

    st.title("My Courses")

    user = st.session_state.get("user") or {}

    db = SessionLocal()

    try:
        courses = (
            db.query(Course)
            .filter(Course.instructor_id == user.get("id"))
            .order_by(Course.created_at.desc())
            .all()
        )

        if not courses:

            st.info("No courses have been added yet.")

        else:

            rows = [
                {
                    "Course": c.course_name,
                    "Section": c.section,
                    "Semester": c.semester,
                    "Students Enrolled": len(c.enrollments),
                }
                for c in courses
            ]

            st.dataframe(rows, use_container_width=True)

    finally:
        db.close()

    if st.button("← Back"):
        st.session_state.page = "instructor_dashboard"
        st.rerun()