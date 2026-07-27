import streamlit as st

from utils.ui import load_css, add_bg_image
from auth.authentication import register_user


def show_register():

    load_css()
    add_bg_image()

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, center, right = st.columns([1, 1, 1])

    with center:

        with st.container(border=True):

            st.markdown(
                """
                <h2 style="text-align:center;color:#4A2E12;">
                Create Account
                </h2>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center;color:gray;'>Register using your university email.</p>",
                unsafe_allow_html=True
            )

            name = st.text_input("Full Name")

            email = st.text_input(
                "University Email",
                placeholder="example@northsouth.edu"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            confirm = st.text_input(
                "Confirm Password",
                type="password"
            )

            # Create Account Button
            if st.button(
                "Create Account",
                use_container_width=True,
                key="create"
            ):

                success, message = register_user(
                    name,
                    email,
                    password,
                    confirm
                )

                if success:
                    st.success(message)
                else:
                    st.error(message)

            st.markdown("<br>", unsafe_allow_html=True)

            # Back to Login Button
            if st.button(
                "← Back to Login",
                use_container_width=True,
                key="back"
            ):
                st.session_state.page = "login"
                st.rerun()

            st.markdown(
                "<p class='footer'>© North South University</p>",
                unsafe_allow_html=True
            )