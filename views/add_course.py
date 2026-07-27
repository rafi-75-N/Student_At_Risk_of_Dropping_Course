import streamlit as st

from utils.ui import load_css


def show_add_course():

    load_css()

    st.title("Add Course")

    course = st.text_input("Course Name")

    section = st.text_input("Section")

    semester = st.text_input("Semester")

    if st.button("Create Course"):

        st.success("Course created successfully!")

    if st.button("← Back"):

        st.session_state.page = "instructor_dashboard"

        st.rerun()