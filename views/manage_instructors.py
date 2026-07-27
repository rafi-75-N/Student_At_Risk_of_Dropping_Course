import streamlit as st

from utils.ui import load_css


def show_manage_instructors():

    load_css()

    st.title("Manage Instructors")

    st.markdown("---")

    instructors = [
        {
            "Instructor ID": "INS001",
            "Name": "Dr. Ahmed",
            "Email": "ahmed@northsouth.edu"
        },
        {
            "Instructor ID": "INS002",
            "Name": "Dr. Hasan",
            "Email": "hasan@northsouth.edu"
        },
        {
            "Instructor ID": "INS003",
            "Name": "Dr. Islam",
            "Email": "islam@northsouth.edu"
        }
    ]

    st.subheader("Instructor List")

    st.dataframe(
        instructors,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("Instructor Details")

    instructor_id = st.text_input("Instructor ID")

    instructor_name = st.text_input("Instructor Name")

    instructor_email = st.text_input("Email")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "Add Instructor",
            use_container_width=True
        ):
            st.success("Instructor Added Successfully!")

    with col2:

        if st.button(
            "Update Instructor",
            use_container_width=True
        ):
            st.success("Instructor Updated Successfully!")

    with col3:

        if st.button(
            "Delete Instructor",
            use_container_width=True
        ):
            st.warning("Instructor Deleted!")

    st.markdown("---")

    if st.button(
        "← Back",
        use_container_width=True
    ):
        st.session_state.page = "admin_dashboard"
        st.rerun()