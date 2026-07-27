import base64
import streamlit as st


def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


def add_bg_image():

    with open("assets/background.jpeg", "rb") as image:

        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{

            background-image:
            linear-gradient(
                rgba(0,0,0,0.70),
                rgba(0,0,0,0.70)
            ),
            url("data:image/jpeg;base64,{encoded}");

            background-size:cover;
            background-position:center;
            background-repeat:no-repeat;

        }}

        </style>
        """,
        unsafe_allow_html=True
    )