import streamlit as st

from utils.ui import load_css


def show_view_courses():

    load_css()

    st.title("My Courses")

    st.info("No courses have been added yet.")

    if st.button("← Back"):
        st.session_state.page = "instructor_dashboard"
        st.rerun()