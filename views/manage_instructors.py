import streamlit as st

from utils.ui import load_css
from utils import api_client


def show_manage_instructors():

    load_css()

    st.title("Manage Instructors")

    st.markdown("---")

    try:
        instructors = api_client.list_instructors()
    except Exception:
        st.error("Couldn't reach the server. Is the API running?")
        instructors = []

    st.subheader("Instructor List")

    if instructors:

        rows = [
            {"Name": i["name"], "Email": i["email"], "Courses": i["count"]}
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

            else:

                try:
                    result = api_client.add_staff("instructor", instructor_name, instructor_email, temp_password)

                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])

                except Exception:
                    st.error("Couldn't reach the server. Is the API running?")

    with col2:

        if st.button("Update Instructor", use_container_width=True):

            try:
                result = api_client.update_staff("instructor", instructor_email, instructor_name or None)

                if result["success"]:
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])

            except Exception:
                st.error("Couldn't reach the server. Is the API running?")

    with col3:

        if st.button("Delete Instructor", use_container_width=True):

            try:
                result = api_client.delete_staff("instructor", instructor_email)

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
