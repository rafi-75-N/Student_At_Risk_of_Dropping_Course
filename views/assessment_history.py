import streamlit as st

from utils.ui import load_css


def show_assessment_history():

    load_css()

    st.title("Assessment History")

    st.markdown("---")

    history = [

        {
            "Student ID": "2232205",
            "Student Name": "Ashfak",
            "Sleep Hours": 7,
            "Internet Usage": 5,
            "Stress Level": 6
        },

        {
            "Student ID": "22112000",
            "Student Name": "Tawsif",
            "Sleep Hours": 6,
            "Internet Usage": 8,
            "Stress Level": 8
        },

        {
            "Student ID": "2323006",
            "Student Name": "Rafi",
            "Sleep Hours": 8,
            "Internet Usage": 4,
            "Stress Level": 3
        }

    ]

    st.dataframe(
        history,
        use_container_width=True
    )

    st.markdown("")

    if st.button(
        "Back",
        use_container_width=True
    ):

        st.session_state.page = "doctor_dashboard"

        st.rerun()