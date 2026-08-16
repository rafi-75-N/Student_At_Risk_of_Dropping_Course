import streamlit as st

from utils.ui import load_css
from api.db import SessionLocal
from api.models import User, Course
from auth.authentication import get_role_from_email, hash_password


def show_manage_instructors():

    load_css()

    st.title("Manage Instructors")

    st.markdown("---")

    db = SessionLocal()

    try:
        instructors = (
            db.query(User)
            .filter(User.role == "instructor")
            .order_by(User.name)
            .all()
        )

        st.subheader("Instructor List")

        if instructors:

            rows = [
                {
                    "Name": i.name,
                    "Email": i.email,
                    "Courses": db.query(Course)
                        .filter(Course.instructor_id == i.id)
                        .count(),
                }
                for i in instructors
            ]

            st.dataframe(rows, use_container_width=True)

        else:

            st.info("No instructors registered yet.")

        st.markdown("---")

        st.subheader("Instructor Details")

        instructor_email = st.text_input("Instructor Email")

        instructor_name = st.text_input("Instructor Name")

        temp_password = st.text_input(
            "Temporary Password (only needed to Add a new instructor)",
            type="password"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button("Add Instructor", use_container_width=True):

                if not instructor_email or not instructor_name or not temp_password:

                    st.error("Name, email, and a temporary password are required.")

                elif get_role_from_email(instructor_email) != "instructor":

                    st.error("Email must end in @northsouth.edu for an instructor account.")

                else:

                    existing = (
                        db.query(User)
                        .filter(User.email.ilike(instructor_email))
                        .first()
                    )

                    if existing:

                        st.error("An account with this email already exists.")

                    else:

                        db.add(User(
                            name=instructor_name,
                            email=instructor_email,
                            password_hash=hash_password(temp_password),
                            role="instructor",
                        ))

                        db.commit()

                        st.success(
                            "Instructor added. Share the temporary password "
                            "with them directly so they can log in."
                        )

                        st.rerun()

        with col2:

            if st.button("Update Instructor", use_container_width=True):

                instructor = (
                    db.query(User)
                    .filter(
                        User.email.ilike(instructor_email),
                        User.role == "instructor",
                    )
                    .first()
                )

                if not instructor:

                    st.error("No instructor found with that email.")

                else:

                    if instructor_name:
                        instructor.name = instructor_name

                    db.commit()

                    st.success("Instructor Updated Successfully!")

                    st.rerun()

        with col3:

            if st.button("Delete Instructor", use_container_width=True):

                instructor = (
                    db.query(User)
                    .filter(
                        User.email.ilike(instructor_email),
                        User.role == "instructor",
                    )
                    .first()
                )

                if not instructor:

                    st.error("No instructor found with that email.")

                else:

                    has_courses = (
                        db.query(Course)
                        .filter(Course.instructor_id == instructor.id)
                        .first()
                        is not None
                    )

                    if has_courses:

                        st.error(
                            "Can't delete: this instructor has courses on "
                            "record. Reassign or remove those first."
                        )

                    else:

                        db.delete(instructor)
                        db.commit()

                        st.warning("Instructor Deleted!")

                        st.rerun()

    finally:
        db.close()

    st.markdown("---")

    if st.button("← Back", use_container_width=True):
        st.session_state.page = "admin_dashboard"
        st.rerun()