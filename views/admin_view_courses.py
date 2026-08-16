import streamlit as st

from utils.ui import load_css
from api.db import SessionLocal
from api.models import Course, Enrollment, StudentProfile, StudentAssessment


def show_admin_view_courses():

    load_css()

    st.title("All Courses")

    st.markdown("---")

    db = SessionLocal()

    try:
        courses = (
            db.query(Course)
            .order_by(Course.course_name)
            .all()
        )

        if not courses:

            st.info("No courses have been created yet.")

        else:

            course_labels = {
                f"{c.course_name} — Section {c.section} ({c.semester})": c.id
                for c in courses
            }

            selected_label = st.selectbox(
                "Select a Course",
                list(course_labels.keys())
            )

            course_id = course_labels[selected_label]

            st.markdown("---")

            st.subheader(f"Students Enrolled in {selected_label}")

            enrollments = (
                db.query(Enrollment)
                .join(StudentProfile)
                .filter(Enrollment.course_id == course_id)
                .all()
            )

            if not enrollments:

                st.info("No students enrolled in this course yet.")

            else:

                rows = []

                for e in enrollments:

                    # Pull in the student's most recent doctor assessment,
                    # if one exists — this is the "combination of the two
                    # people" (instructor's academic data + doctor's
                    # wellness data) in one row.
                    latest_assessment = (
                        db.query(StudentAssessment)
                        .filter(StudentAssessment.student_id == e.student_id)
                        .order_by(StudentAssessment.created_at.desc())
                        .first()
                    )

                    rows.append({
                        "Student ID": e.student.student_id,
                        "Name": e.student.name,
                        "Attendance (%)": e.attendance,
                        "Quiz": e.quiz_marks,
                        "Mid": e.mid_marks,
                        "Sleep Hours": latest_assessment.sleep_hours if latest_assessment else None,
                        "Internet Usage": latest_assessment.internet_usage_hours if latest_assessment else None,
                        "Stress Level": latest_assessment.stress_level if latest_assessment else None,
                    })

                st.dataframe(rows, use_container_width=True)

                st.caption(
                    "Sleep Hours / Internet Usage / Stress Level are blank for "
                    "students a doctor hasn't assessed yet."
                )

    finally:
        db.close()

    st.markdown("")

    if st.button("← Back", use_container_width=True):
        st.session_state.page = "admin_dashboard"
        st.rerun()