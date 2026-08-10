import streamlit as st

from utils.ui import load_css
from api.db import SessionLocal
from api.models import Course, StudentProfile, Enrollment


def show_manage_course():

    load_css()

    st.title("Manage Courses")

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

            st.info("No courses available. Add one first from 'Add Course'.")

        else:

            course_labels = {
                f"{c.course_name} — Section {c.section} ({c.semester})": c.id
                for c in courses
            }

            selected_label = st.selectbox(
                "Select a Course",
                list(course_labels.keys()),
            )

            course_id = course_labels[selected_label]

            st.markdown("---")

            st.subheader("Enrolled Students")

            enrollments = (
                db.query(Enrollment)
                .join(StudentProfile)
                .filter(Enrollment.course_id == course_id)
                .all()
            )

            if enrollments:

                rows = [
                    {
                        "Student ID": e.student.student_id,
                        "Name": e.student.name,
                        "Attendance (%)": e.attendance,
                        "Quiz": e.quiz_marks,
                        "Mid": e.mid_marks,
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

                attendance = st.number_input(
                    "Attendance (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0,
                    key="mc_attendance",
                )

                quiz_marks = st.number_input(
                    "Quiz Marks",
                    min_value=0.0,
                    step=1.0,
                    key="mc_quiz",
                )

                mid_marks = st.number_input(
                    "Mid Marks",
                    min_value=0.0,
                    step=1.0,
                    key="mc_mid",
                )

            col_a, col_b = st.columns(2)

            with col_a:

                if st.button("Save Record", use_container_width=True):

                    if not student_id or not student_name:

                        st.error("Student ID and Name are required.")

                    else:

                        student = (
                            db.query(StudentProfile)
                            .filter(StudentProfile.student_id == student_id)
                            .first()
                        )

                        if not student:

                            student = StudentProfile(
                                student_id=student_id,
                                name=student_name,
                                email=student_email or None,
                            )

                            db.add(student)
                            db.flush()  # assigns student.id before we use it below

                        else:

                            student.name = student_name

                            if student_email:
                                student.email = student_email

                        enrollment = (
                            db.query(Enrollment)
                            .filter(
                                Enrollment.course_id == course_id,
                                Enrollment.student_id == student.id,
                            )
                            .first()
                        )

                        if not enrollment:

                            enrollment = Enrollment(
                                course_id=course_id,
                                student_id=student.id,
                            )

                            db.add(enrollment)

                        enrollment.attendance = attendance
                        enrollment.quiz_marks = quiz_marks
                        enrollment.mid_marks = mid_marks

                        db.commit()

                        st.success(f"Record saved for {student_name}.")

                        st.rerun()

            with col_b:

                if st.button("Remove Student from Course", use_container_width=True):

                    if not student_id:

                        st.error("Enter the Student ID to remove.")

                    else:

                        student = (
                            db.query(StudentProfile)
                            .filter(StudentProfile.student_id == student_id)
                            .first()
                        )

                        if student:

                            db.query(Enrollment).filter(
                                Enrollment.course_id == course_id,
                                Enrollment.student_id == student.id,
                            ).delete()

                            db.commit()

                            st.warning(f"Removed {student_id} from this course.")

                            st.rerun()

                        else:

                            st.error("No such student found.")

    finally:
        db.close()

    st.markdown("---")

    if st.button("← Back", use_container_width=True):

        st.session_state.page = "instructor_dashboard"

        st.rerun()