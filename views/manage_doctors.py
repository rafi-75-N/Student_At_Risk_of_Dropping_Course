import streamlit as st

from utils.ui import load_css
from utils import api_client


def show_manage_doctors():

    load_css()

    st.title("Manage Doctors")

    st.markdown("---")

    try:
        doctors = api_client.list_doctors()
    except Exception:
        st.error("Couldn't reach the server. Is the API running?")
        doctors = []

    st.subheader("Doctor List")

    if doctors:

        rows = [
            {
                "Name": d["name"],
                "Email": d["email"],
                "Specialization": d["specialization"] or "",
                "Assessments": d["count"],
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

            else:

                try:
                    result = api_client.add_staff("doctor", doctor_name, doctor_email, temp_password, specialization)

                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])

                except Exception:
                    st.error("Couldn't reach the server. Is the API running?")

    with col2:

        if st.button("Update Doctor", use_container_width=True):

            try:
                result = api_client.update_staff("doctor", doctor_email, doctor_name or None, specialization)

                if result["success"]:
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])

            except Exception:
                st.error("Couldn't reach the server. Is the API running?")

    with col3:

        if st.button("Delete Doctor", use_container_width=True):

            try:
                result = api_client.delete_staff("doctor", doctor_email)

                if result["success"]:
                    st.warning(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])

            except Exception:
                st.error("Couldn't reach the server. Is the API running?")

    st.markdown("---")

    if st.button("← Back", use_container_width=True):
        st.session_state.page = "admin_dashboard"
        st.rerun()
