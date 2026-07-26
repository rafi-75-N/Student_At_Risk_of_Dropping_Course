import streamlit as st

from utils.ui import load_css


def show_manage_course():

    load_css()

    st.title("Manage Courses")

    st.info("No courses available.")

    if st.button("← Back"):

        st.session_state.page = "instructor_dashboard"

        st.rerun()