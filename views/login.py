import streamlit as st

from utils.ui import load_css, add_bg_image
from auth.authentication import login_user


def show_login():

    load_css()
    add_bg_image()

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, center, right = st.columns([1,1,1])

    with center:

        with st.container(border=True):

            st.image("assets/logo.png", width=90)

            st.markdown(
                """
                <h2 style="text-align:center;color:#4A2E12;">
                Student Dropout
                <br>
                Prediction System
                </h2>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                "<p style='text-align:center;color:gray;'>Sign in to continue</p>",
                unsafe_allow_html=True
            )

            email = st.text_input(
                "University Email",
                placeholder="example@northsouth.edu"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button(
                "Login",
                use_container_width=True,
                key="login"
            ):

                success, result = login_user(email, password)

                if success:
                    st.session_state.user = result

                    role = result["role"]

                    if role == "instructor":
                        st.session_state.page = "instructor_dashboard"
                    elif role == "admin":
                        st.session_state.page = "admin_dashboard"
                    elif role == "doctor":
                        st.session_state.page = "doctor_dashboard"

                    st.rerun()

                else:
                    st.error(result)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(
                """
                <p style="
                    text-align:center;
                    color:#4A2E12;
                    font-weight:bold;
                    font-size:17px;
                ">
                Don't have an account?
                </p>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Register",
                use_container_width=True,
                key="register"
            ):
                st.session_state.page = "register"
                st.rerun()