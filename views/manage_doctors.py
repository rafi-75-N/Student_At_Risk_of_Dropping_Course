import streamlit as st

from utils.ui import load_css


def show_manage_doctors():

    load_css()

    st.title("Manage Doctors")

    st.markdown("---")

    doctors = [

        {
            "Doctor ID": "DOC001",
            "Name": "Dr. Rahman",
            "Email": "rahman@docnorthsouth.edu",
            "Specialization": "Psychologist"
        },

        {
            "Doctor ID": "DOC002",
            "Name": "Dr. Ahmed",
            "Email": "ahmed@docnorthsouth.edu",
            "Specialization": "Psychiatrist"
        },

        {
            "Doctor ID": "DOC003",
            "Name": "Dr. Karim",
            "Email": "karim@docnorthsouth.edu",
            "Specialization": "Counselor"
        }

    ]

    st.subheader("Doctor List")

    st.dataframe(
        doctors,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("Doctor Details")

    doctor_id = st.text_input(
        "Doctor ID"
    )

    doctor_name = st.text_input(
        "Doctor Name"
    )

    doctor_email = st.text_input(
        "Email"
    )

    specialization = st.selectbox(
        "Specialization",
        [
            "Psychologist",
            "Psychiatrist",
            "Counselor",
            "Medical Officer",
            "Other"
        ]
    )

    st.markdown("")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "Add Doctor",
            use_container_width=True
        ):

            st.success("Doctor Added Successfully!")

    with col2:

        if st.button(
            "Update Doctor",
            use_container_width=True
        ):

            st.success("Doctor Updated Successfully!")

    with col3:

        if st.button(
            "Delete Doctor",
            use_container_width=True
        ):

            st.warning("Doctor Deleted!")

    st.markdown("---")

    if st.button(
        "← Back",
        use_container_width=True
    ):

        st.session_state.page = "admin_dashboard"

        st.rerun()