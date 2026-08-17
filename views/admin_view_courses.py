import streamlit as st

from utils.ui import load_css
from utils import api_client


def show_admin_view_courses():

    load_css()

    st.title("All Courses")

    st.markdown("---")

    try:
        courses = api_client.list_courses()
    except Exception:
        st.error("Couldn't reach the server. Is the API running?")
        courses = []

    if not courses:

        st.info("No courses have been created yet.")

    else:

        course_labels = {
            f"{c['course_name']} — Section {c['section']} ({c['semester']})": c["id"]
            for c in courses
        }

        selected_label = st.selectbox("Select a Course", list(course_labels.keys()))

        course_id = course_labels[selected_label]

        st.markdown("---")

        st.subheader(f"Students Enrolled in {selected_label}")

        try:
            rows_data = api_client.combined_course_view(course_id)
        except Exception:
            st.error("Couldn't reach the server. Is the API running?")
            rows_data = []

        if not rows_data:

            st.info("No students enrolled in this course yet.")

        else:

            rows = [
                {
                    "Student ID": r["student_id"],
                    "Name": r["name"],
                    "Midterm": r["midterm_score"],
                    "Assignments": r["assignments_avg"],
                    "Quizzes": r["quizzes_avg"],
                    "Participation": r["participation_score"],
                    "Projects": r["projects_score"],
                    "Attendance (%)": r["attendance"],
                    "Study Hours": r["study_hours"],
                    "Sleep Hours": r["sleep_hours"],
                    "Stress Level": r["stress_level"],
                    "Instructor Marks (/75)": r["instructor_marks"],
                    "Doctor Marks (/25)": r["doctor_marks"],
                    "Predicted Score": r["performance_score"],
                    "Doctor Effect": r["doctor_effect"],
                    "Grade": r["grade"],
                    "Risk Level": r["risk_level"],
                }
                for r in rows_data
            ]

            st.dataframe(rows, use_container_width=True)

            model_is_live = any(r["doctor_effect"] is not None for r in rows_data)

            if model_is_live:
                st.caption(
#                   "Predicted Score comes from the trained XGBoost model. Doctor "
  #                  "Effect shows how many points a student's score shifts because "
   #                 "of their doctor assessment specifically (vs. an average one) — "
    #                "positive means it's helping them, negative means it's hurting them. "
     #               "Risk Level: No Risk (≥75), Medium Risk (60–74.99), High Risk (<60)."
                )
            else:
                st.caption(
        #            "Predicted Score is currently the plain formula (XGBoost model "
         #           "not trained yet — run train_model.py). Doctor Effect will appear "
          #          "once it is. Blank rows mean instructor or doctor data is incomplete."
                )

    st.markdown("")

    if st.button("← Back", use_container_width=True):
        st.session_state.page = "admin_dashboard"
        st.rerun()
