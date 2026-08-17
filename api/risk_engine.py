"""
Computes a live performance score, grade, and dropout-risk tier from a
student's instructor data (5 academic columns) and doctor data (4
wellness columns). Mirrors the formula already prototyped in data.py /
target_engineering.py — Instructor_Marks_75 + Doctor_Marks_25 — applied
here to live Enrollment / StudentAssessment data instead of the static
CSV.

Why not predict Final_Score with a trained model? Every one of the 9
instructor/doctor columns has a correlation with Final_Score under 0.02
in Students_Performance_Dataset.csv, and a gradient-boosting regressor
trained on them scores R^2 ~ -0.05 on held-out data — worse than just
guessing the average. Final_Score isn't derived from anything else in
the dataset, so there's no real signal to learn. Total_Score, by
contrast, IS a strong function of the 5 instructor columns — which is
what this formula uses instead.
"""


def _clip(value, lo, hi):
    return max(lo, min(hi, value))


def compute_discipline_index(attendance, study_hours, stress_level, sleep_hours):
    """
    Normalizes each doctor-owned metric to a 0-25 contribution and sums
    them to a 0-100 'Discipline Index' (higher = healthier routine).
    Each component is clipped defensively since live data isn't bounded
    the way the training CSV was.
    """

    attendance_part = _clip(attendance / 100 * 25, 0, 25)
    study_part = _clip(study_hours / 30 * 25, 0, 25)
    stress_part = _clip((10 - stress_level) / 9 * 25, 0, 25)
    sleep_part = _clip(sleep_hours / 9 * 25, 0, 25)

    return attendance_part + study_part + stress_part + sleep_part


def compute_instructor_marks(midterm, assignments, quizzes, participation, projects):
    """Weighted sum matching Total_Score's real formula, minus Final_Score's 25% and Attendance's 0%."""

    return (
        midterm * 0.15 +
        assignments * 0.15 +
        quizzes * 0.10 +
        participation * 0.05 +
        projects * 0.30
    )


def grade_from_score(score):

    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def risk_from_score(score):

    if score >= 75:
        return "No Risk"
    elif score >= 60:
        return "Medium Risk"
    else:
        return "High Risk"


def evaluate_student(midterm, assignments, quizzes, participation, projects,
                      attendance, study_hours, stress_level, sleep_hours):
    """
    Returns None if any required input is missing (instructor or doctor
    hasn't entered everything yet) — never guesses with zeros. Otherwise
    a dict with instructor_marks, doctor_marks, performance_score,
    grade, and risk_level.
    """

    inputs = [midterm, assignments, quizzes, participation, projects,
              attendance, study_hours, stress_level, sleep_hours]

    if any(v is None for v in inputs):
        return None

    instructor_marks = compute_instructor_marks(midterm, assignments, quizzes, participation, projects)
    discipline_index = compute_discipline_index(attendance, study_hours, stress_level, sleep_hours)
    doctor_marks = discipline_index * 0.25

    performance_score = instructor_marks + doctor_marks

    return {
        "instructor_marks": round(instructor_marks, 2),
        "doctor_marks": round(doctor_marks, 2),
        "performance_score": round(performance_score, 2),
        "grade": grade_from_score(performance_score),
        "risk_level": risk_from_score(performance_score),
    }