import streamlit as st

from utils.ui import load_css
from utils import api_client


def show_manage_course():

    load_css()

    st.title("Manage Courses")

    user = st.session_state.get("user") or {}

    try:
        courses = api_client.list_courses(instructor_id=user.get("id"))

    except Exception:
        st.error("Couldn't reach the server. Is the API running?")
        courses = []

    if not courses:

        st.info("No courses available. Add one first from 'Add Course'.")

    else:

        course_labels = {
            f"{c['course_name']} — Section {c['section']} ({c['semester']})": c["id"]
            for c in courses
        }

        selected_label = st.selectbox("Select a Course", list(course_labels.keys()))

        course_id = course_labels[selected_label]

        st.markdown("---")

        st.subheader("Enrolled Students")

        try:
            enrollments = api_client.list_enrollments(course_id)
        except Exception:
            st.error("Couldn't reach the server. Is the API running?")
            enrollments = []

        if enrollments:

            rows = [
                {
                    "Student ID": e["student_id"],
                    "Name": e["name"],
                    "Midterm": e["midterm_score"],
                    "Assignments": e["assignments_avg"],
                    "Quizzes": e["quizzes_avg"],
                    "Participation": e["participation_score"],
                    "Projects": e["projects_score"],
                }
                for e in enrollments
            ]

            st.dataframe(rows, use_container_width=True)

        else:

            st.info("No students enrolled in this course yet.")

        st.markdown("---")

        st.subheader("Add / Update a Student's Record")

        col1, col2 = st.columns(2)

        with col1:

            student_id = st.text_input("Student ID", key="mc_student_id")
            student_name = st.text_input("Student Name", key="mc_student_name")
            student_email = st.text_input("Email (optional)", key="mc_student_email")

        with col2:

            midterm_score = st.number_input("Midterm Score", min_value=0.0, max_value=100.0, step=1.0, key="mc_midterm")
            assignments_avg = st.number_input("Assignments Avg", min_value=0.0, max_value=100.0, step=1.0, key="mc_assign")
            quizzes_avg = st.number_input("Quizzes Avg", min_value=0.0, max_value=100.0, step=1.0, key="mc_quiz")
            participation_score = st.number_input("Participation Score", min_value=0.0, max_value=100.0, step=1.0, key="mc_part")
            projects_score = st.number_input("Projects Score", min_value=0.0, max_value=100.0, step=1.0, key="mc_proj")

        col_a, col_b = st.columns(2)

        with col_a:

            if st.button("Save Record", use_container_width=True):

                if not student_id or not student_name:

                    st.error("Student ID and Name are required.")

                else:

                    try:
                        result = api_client.upsert_enrollment(
                            course_id, student_id, student_name, student_email or None,
                            midterm_score, assignments_avg, quizzes_avg,
                            participation_score, projects_score,
                        )

                        if result["success"]:
                            st.success(result["message"])
                            st.rerun()
                        else:
                            st.error(result["message"])

                    except Exception:
                        st.error("Couldn't reach the server. Is the API running?")

        with col_b:

            if st.button("Remove Student from Course", use_container_width=True):

                if not student_id:

                    st.error("Enter the Student ID to remove.")

                else:

                    try:
                        result = api_client.remove_enrollment(course_id, student_id)

                        if result["success"]:
                            st.warning(result["message"])
                            st.rerun()
                        else:
                            st.error(result["message"])

                    except Exception:
                        st.error("Couldn't reach the server. Is the API running?")

    st.markdown("---")

    if st.button("← Back", use_container_width=True):

        st.session_state.page = "instructor_dashboard"

        st.rerun()
