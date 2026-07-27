import streamlit as st

from utils.ui import load_css


def show_admin_view_courses():

    load_css()

    st.title("All Courses")

    st.markdown("---")

    courses = [
        "CSE115",
        "CSE215",
        "CSE299",
        "CSE327"
    ]

    selected_course = st.selectbox(

        "Select a Course",

        courses

    )

    st.markdown("---")

    st.subheader(f"Students Enrolled in {selected_course}")

    students = [

        {
            "Student ID": "22100001",
            "Name": "Ashfak",
            "Attendance": 92,
            "Quiz": 18,
            "Mid": 24,
            "Sleep Hours": 7,
            "Internet Usage": 5,
            "Stress Level": 4
        },

        {
            "Student ID": "22100002",
            "Name": "Tawsif",
            "Attendance": 85,
            "Quiz": 16,
            "Mid": 22,
            "Sleep Hours": 6,
            "Internet Usage": 8,
            "Stress Level": 7
        },

        {
            "Student ID": "22100003",
            "Name": "Rafi",
            "Attendance": 97,
            "Quiz": 20,
            "Mid": 25,
            "Sleep Hours": 8,
            "Internet Usage": 3,
            "Stress Level": 2
        }

    ]

    st.dataframe(
        students,
        use_container_width=True
    )

    st.markdown("")

    if st.button(
        "← Back",
        use_container_width=True
    ):

        st.session_state.page = "admin_dashboard"

        st.rerun()