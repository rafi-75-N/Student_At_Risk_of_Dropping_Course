import streamlit as st

from utils.ui import load_css
from api.db import SessionLocal
from api.models import User, StudentAssessment
from auth.authentication import get_role_from_email, hash_password


def show_manage_doctors():

    load_css()

    st.title("Manage Doctors")

    st.markdown("---")

    db = SessionLocal()

    try:
        doctors = (
            db.query(User)
            .filter(User.role == "doctor")
            .order_by(User.name)
            .all()
        )

        st.subheader("Doctor List")

        if doctors:

            rows = [
                {
                    "Name": d.name,
                    "Email": d.email,
                    "Specialization": d.specialization or "",
                    "Assessments": db.query(StudentAssessment)
                        .filter(StudentAssessment.doctor_id == d.id)
                        .count(),
                }
                for d in doctors
            ]

            st.dataframe(rows, use_container_width=True)

        else:

            st.info("No doctors registered yet.")

        st.markdown("---")

        st.subheader("Doctor Details")

        doctor_email = st.text_input("Doctor Email")

        doctor_name = st.text_input("Doctor Name")

        specialization = st.selectbox(
            "Specialization",
            ["Psychologist", "Psychiatrist", "Counselor", "Medical Officer", "Other"]
        )

        temp_password = st.text_input(
            "Temporary Password (only needed to Add a new doctor)",
            type="password"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button("Add Doctor", use_container_width=True):

                if not doctor_email or not doctor_name or not temp_password:

                    st.error("Name, email, and a temporary password are required.")

                elif get_role_from_email(doctor_email) != "doctor":

                    st.error("Email must end in @docnorthsouth.edu for a doctor account.")

                else:

                    existing = (
                        db.query(User)
                        .filter(User.email.ilike(doctor_email))
                        .first()
                    )

                    if existing:

                        st.error("An account with this email already exists.")

                    else:

                        db.add(User(
                            name=doctor_name,
                            email=doctor_email,
                            password_hash=hash_password(temp_password),
                            role="doctor",
                            specialization=specialization,
                        ))

                        db.commit()

                        st.success(
                            "Doctor added. Share the temporary password "
                            "with them directly so they can log in."
                        )

                        st.rerun()

        with col2:

            if st.button("Update Doctor", use_container_width=True):

                doctor = (
                    db.query(User)
                    .filter(
                        User.email.ilike(doctor_email),
                        User.role == "doctor",
                    )
                    .first()
                )

                if not doctor:

                    st.error("No doctor found with that email.")

                else:

                    if doctor_name:
                        doctor.name = doctor_name

                    doctor.specialization = specialization

                    db.commit()

                    st.success("Doctor Updated Successfully!")

                    st.rerun()

        with col3:

            if st.button("Delete Doctor", use_container_width=True):

                doctor = (
                    db.query(User)
                    .filter(
                        User.email.ilike(doctor_email),
                        User.role == "doctor",
                    )
                    .first()
                )

                if not doctor:

                    st.error("No doctor found with that email.")

                else:

                    has_assessments = (
                        db.query(StudentAssessment)
                        .filter(StudentAssessment.doctor_id == doctor.id)
                        .first()
                        is not None
                    )

                    if has_assessments:

                        st.error(
                            "Can't delete: this doctor has assessments on "
                            "record. Remove those first."
                        )

                    else:

                        db.delete(doctor)
                        db.commit()

                        st.warning("Doctor Deleted!")

                        st.rerun()

    finally:
        db.close()

    st.markdown("---")

    if st.button("← Back", use_container_width=True):
        st.session_state.page = "admin_dashboard"
        st.rerun()