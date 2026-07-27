import streamlit as st

from utils.ui import load_css


def show_instructor_dashboard():

    load_css()

    st.title(" Instructor Dashboard")

    st.markdown("---")

    st.subheader("Welcome!")

    st.write("Choose one of the following options.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("###  View Courses")

        if st.button(
            "Open",
            use_container_width=True,
            key="view_courses"
        ):
            st.session_state.page = "view_courses"
            st.rerun()

    with col2:
        st.markdown("###  Add Course")

        if st.button(
            "Open",
            use_container_width=True,
            key="add_course"
        ):
            st.session_state.page = "add_course"
            st.rerun()

    with col3:
        st.markdown("###  Manage Course")

        if st.button(
            "Open",
            use_container_width=True,
            key="manage_course"
        ):
            st.session_state.page = "manage_course"
            st.rerun()

    st.markdown("---")

    if st.button("Logout"):
        st.session_state.page = "login"
        st.rerun()