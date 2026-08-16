import streamlit as st

from utils.ui import load_css
from api.db import SessionLocal
from api.models import StudentProfile, Enrollment, StudentAssessment


def show_manage_students():

    load_css()

    st.title("Manage Students")

    st.markdown("---")

    db = SessionLocal()

    try:
        students = (
            db.query(StudentProfile)
            .order_by(StudentProfile.student_id)
            .all()
        )

        st.subheader("Student List")

        if students:

            rows = [
                {
                    "Student ID": s.student_id,
                    "Name": s.name,
                    "Email": s.email or "",
                    "Department": s.department or "",
                }
                for s in students
            ]

            st.dataframe(rows, use_container_width=True)

        else:

            st.info("No students in the system yet.")

        st.markdown("---")

        st.subheader("Student Details")

        student_id = st.text_input("Student ID")

        student_name = st.text_input("Student Name")

        student_email = st.text_input("Email")

        department = st.selectbox(
            "Department",
            ["CSE", "EEE", "BBA", "LAW", "ECE"]
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button("Add Student", use_container_width=True):

                if not student_id or not student_name:

                    st.error("Student ID and Name are required.")

                else:

                    existing = (
                        db.query(StudentProfile)
                        .filter(StudentProfile.student_id == student_id)
                        .first()
                    )

                    if existing:

                        st.error("A student with this ID already exists.")

                    else:

                        db.add(StudentProfile(
                            student_id=student_id,
                            name=student_name,
                            email=student_email or None,
                            department=department,
                        ))

                        db.commit()

                        st.success("Student Added Successfully!")

                        st.rerun()

        with col2:

            if st.button("Update Student", use_container_width=True):

                student = (
                    db.query(StudentProfile)
                    .filter(StudentProfile.student_id == student_id)
                    .first()
                )

                if not student:

                    st.error("No student found with that ID.")

                else:

                    if student_name:
                        student.name = student_name

                    if student_email:
                        student.email = student_email

                    student.department = department

                    db.commit()

                    st.success("Student Information Updated!")

                    st.rerun()

        with col3:

            if st.button("Delete Student", use_container_width=True):

                student = (
                    db.query(StudentProfile)
                    .filter(StudentProfile.student_id == student_id)
                    .first()
                )

                if not student:

                    st.error("No student found with that ID.")

                else:

                    has_enrollments = (
                        db.query(Enrollment)
                        .filter(Enrollment.student_id == student.id)
                        .first()
                        is not None
                    )

                    has_assessments = (
                        db.query(StudentAssessment)
                        .filter(StudentAssessment.student_id == student.id)
                        .first()
                        is not None
                    )

                    if has_enrollments or has_assessments:

                        st.error(
                            "Can't delete: this student has course or "
                            "assessment records tied to them. Remove those first."
                        )

                    else:

                        db.delete(student)
                        db.commit()

                        st.warning("Student Deleted!")

                        st.rerun()

    finally:
        db.close()

    st.markdown("---")

    if st.button("← Back", use_container_width=True):
        st.session_state.page = "admin_dashboard"
        st.rerun()