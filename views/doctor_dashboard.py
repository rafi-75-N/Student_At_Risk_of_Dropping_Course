import streamlit as st

from utils.ui import load_css


def show_doctor_dashboard():

    load_css()

    st.title("Doctor Dashboard")

    st.markdown("---")

    st.subheader("Welcome Doctor")

    st.write("Choose one of the following options.")

    st.markdown("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### New Student Assessment")

        if st.button(
            "Open",
            use_container_width=True,
            key="new_assessment"
        ):

            st.session_state.page = "new_assessment"

            st.rerun()

    with col2:

        st.markdown("### Edit Student Assessment")

        if st.button(
            "Open",
            use_container_width=True,
            key="edit_assessment"
        ):

            st.session_state.page = "edit_assessment"

            st.rerun()

    with col3:

        st.markdown("### Assessment History")

        if st.button(
            "Open",
            use_container_width=True,
            key="assessment_history"
        ):

            st.session_state.page = "assessment_history"

            st.rerun()

    st.markdown("---")

    if st.button("Logout"):

        st.session_state.page = "login"

        st.rerun()