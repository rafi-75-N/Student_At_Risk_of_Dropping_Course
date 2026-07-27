import streamlit as st

from utils.ui import load_css


def show_admin_dashboard():

    load_css()

    st.title("Admin Dashboard")

    st.markdown("---")

    st.subheader("Welcome Administrator")

    st.write("Select one of the following options.")

    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### View Courses")

        if st.button(
            "Open",
            use_container_width=True,
            key="admin_view_courses"
        ):

            st.session_state.page = "admin_view_courses"
            st.rerun()

    with col2:

        st.markdown("### Manage Students")

        if st.button(
            "Open",
            use_container_width=True,
            key="manage_students"
        ):

            st.session_state.page = "manage_students"
            st.rerun()

    st.markdown("")

    col3, col4 = st.columns(2)

    with col3:

        st.markdown("### Manage Instructors")

        if st.button(
            "Open",
            use_container_width=True,
            key="manage_instructors"
        ):

            st.session_state.page = "manage_instructors"
            st.rerun()

    with col4:

        st.markdown("### Manage Doctors")

        if st.button(
            "Open",
            use_container_width=True,
            key="manage_doctors"
        ):

            st.session_state.page = "manage_doctors"
            st.rerun()

    st.markdown("---")

    if st.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.page = "login"
        st.rerun()