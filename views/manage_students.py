import streamlit as st

from utils.ui import load_css


def show_manage_students():

    load_css()

    st.title("Manage Students")

    st.markdown("---")

    students = [
        {
            "Student ID": "22100001",
            "Name": "Ashfak",
            "Email": "ashfak@northsouth.edu",
            "Department": "CSE"
        },
        {
            "Student ID": "22100002",
            "Name": "Rafi",
            "Email": "rafi@northsouth.edu",
            "Department": "CSE"
        },
        {
            "Student ID": "22100003",
            "Name": "Jannat",
            "Email": "jannat@northsouth.edu",
            "Department": "EEE"
        }
    ]

    st.subheader("Student List")

    st.dataframe(
        students,
        use_container_width=True
    )

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

        if st.button(
            "Add Student",
            use_container_width=True
        ):
            st.success("Student Added Successfully!")

    with col2:

        if st.button(
            "Update Student",
            use_container_width=True
        ):
            st.success("Student Information Updated!")

    with col3:

        if st.button(
            "Delete Student",
            use_container_width=True
        ):
            st.warning("Student Deleted!")

    st.markdown("---")

    if st.button(
        "← Back",
        use_container_width=True
    ):
        st.session_state.page = "admin_dashboard"
        st.rerun()