import streamlit as st

from api.db import init_db

from views.login import show_login
from views.register import show_register
from views.instructor_dashboard import show_instructor_dashboard
from views.view_courses import show_view_courses
from views.add_course import show_add_course
from views.manage_course import show_manage_course
from views.doctor_dashboard import show_doctor_dashboard
from views.new_student_assessment import show_new_student_assessment
from views.edit_student_assessment import show_edit_student_assessment
from views.assessment_history import show_assessment_history
from views.admin_dashboard import show_admin_dashboard
from views.admin_view_courses import show_admin_view_courses
from views.manage_students import show_manage_students
from views.manage_instructors import show_manage_instructors
from views.manage_doctors import show_manage_doctors

st.set_page_config(
    page_title="Student Dropout Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Creates the `users` / `students` tables in Postgres the first time the
# app runs. Does nothing if they already exist, so it's safe on every run.
init_db()

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None

# Which role is allowed to view each page. Anything not listed here
# (login, register) is open to everyone.
PAGE_ROLES = {
    "instructor_dashboard": "instructor",
    "view_courses": "instructor",
    "add_course": "instructor",
    "manage_course": "instructor",
    "doctor_dashboard": "doctor",
    "new_assessment": "doctor",
    "edit_assessment": "doctor",
    "assessment_history": "doctor",
    "admin_dashboard": "admin",
    "admin_view_courses": "admin",
    "manage_students": "admin",
    "manage_instructors": "admin",
    "manage_doctors": "admin",
}

required_role = PAGE_ROLES.get(st.session_state.page)

if required_role and (
    not st.session_state.user
    or st.session_state.user["role"] != required_role
):
    # Not logged in, or logged in as the wrong role for this page.
    st.session_state.page = "login"
    st.session_state.user = None

if st.session_state.page == "login":
    show_login()

elif st.session_state.page == "register":
    show_register()

elif st.session_state.page == "instructor_dashboard":
    show_instructor_dashboard()

elif st.session_state.page == "view_courses":
    show_view_courses()

elif st.session_state.page == "add_course":
    show_add_course()

elif st.session_state.page == "manage_course":
    show_manage_course()

elif st.session_state.page == "doctor_dashboard":
    show_doctor_dashboard()

elif st.session_state.page == "new_assessment":
    show_new_student_assessment()

elif st.session_state.page == "edit_assessment":
    show_edit_student_assessment()

elif st.session_state.page == "assessment_history":
    show_assessment_history()

elif st.session_state.page == "admin_dashboard":
    show_admin_dashboard()

elif st.session_state.page == "admin_view_courses":
    show_admin_view_courses()

elif st.session_state.page == "manage_students":
    show_manage_students()

elif st.session_state.page == "manage_instructors":
    show_manage_instructors()

elif st.session_state.page == "manage_doctors":
    show_manage_doctors()