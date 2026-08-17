import streamlit as st

from utils.ui import load_css
from utils import api_client


def show_manage_students():

    load_css()

    st.title("Manage Students")

    st.markdown("---")

    try:
        students = api_client.list_students()
    except Exception:
        st.error("Couldn't reach the server. Is the API running?")
        students = []

    st.subheader("Student List")

    if students:

        rows = [
            {
                "Student ID": s["student_id"],
                "Name": s["name"],
                "Email": s["email"] or "",
                "Department": s["department"] or "",
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

    department = st.selectbox("Department", ["CSE", "EEE", "BBA", "LAW", "ECE"])

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("Add Student", use_container_width=True):

            if not student_id or not student_name:

                st.error("Student ID and Name are required.")

            else:

                try:
                    result = api_client.add_student(student_id, student_name, student_email or None, department)

                    if result["success"]:
                        st.success(result["message"])
                        st.rerun()
                    else:
                        st.error(result["message"])

                except Exception:
                    st.error("Couldn't reach the server. Is the API running?")

    with col2:

        if st.button("Update Student", use_container_width=True):

            try:
                result = api_client.update_student(student_id, student_name or None, student_email or None, department)

                if result["success"]:
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])

            except Exception:
                st.error("Couldn't reach the server. Is the API running?")

    with col3:

        if st.button("Delete Student", use_container_width=True):

            try:
                result = api_client.delete_student(student_id)

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
