"""
Loads the XGBoost model trained by train_model.py (project root) and
exposes a prediction that includes a doctor-effect counterfactual: how
much a student's predicted score changes if their doctor assessment is
swapped out for the class-average one, holding instructor marks fixed.
That isolates "the effect of the doctor's assessment on the final
score" per student.
"""

import os

import joblib
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml", "performance_model.joblib")

_artifact = None
_load_attempted = False


def _load():
    global _artifact, _load_attempted

    if not _load_attempted:
        _load_attempted = True

        if os.path.exists(MODEL_PATH):
            _artifact = joblib.load(MODEL_PATH)

    return _artifact


def is_model_available():
    return _load() is not None


def predict(midterm, assignments, quizzes, participation, projects,
            attendance, study_hours, stress_level, sleep_hours):
    """
    Returns (predicted_score, doctor_effect), or None if train_model.py
    hasn't been run yet.
    """

    artifact = _load()

    if artifact is None:
        return None

    model = artifact["model"]
    feature_order = artifact["feature_order"]
    doctor_cols = artifact["doctor_cols"]
    doctor_baseline = artifact["doctor_baseline_means"]

    row = {
        "Midterm_Score": midterm,
        "Assignments_Avg": assignments,
        "Quizzes_Avg": quizzes,
        "Participation_Score": participation,
        "Projects_Score": projects,
        "Attendance (%)": attendance,
        "Study_Hours_per_Week": study_hours,
        "Stress_Level (1-10)": stress_level,
        "Sleep_Hours_per_Night": sleep_hours,
    }

    full_df = pd.DataFrame([row])[feature_order]
    predicted_score = float(model.predict(full_df)[0])

    baseline_row = dict(row)
    for col in doctor_cols:
        baseline_row[col] = doctor_baseline[col]

    baseline_df = pd.DataFrame([baseline_row])[feature_order]
    baseline_score = float(model.predict(baseline_df)[0])

    doctor_effect = predicted_score - baseline_score

    return round(predicted_score, 2), round(doctor_effect, 2)
