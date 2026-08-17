"""
Trains an XGBoost regressor to predict each student's Total_Marks_100
(the Instructor_Marks_75 + Doctor_Marks_25 composite from
target_engineering.py) from the 9 instructor + doctor columns, and
saves it for the API to load.

Why predict Total_Marks_100 and not the dataset's raw Final_Score
column? Final_Score has ~zero correlation with every other column in
this dataset (checked: max |correlation| = 0.014, a gradient-boosting
model scores R^2 ~ -0.05 trying to learn it) -- there's no real signal
there to learn. Total_Marks_100 is a genuine, strong function of both
groups (instructor columns correlate 0.21-0.67 with it, doctor columns
correlate 0.13-0.29), so it's what a model can actually learn and what
genuinely reflects the doctor's assessment's effect on the outcome.

Run once, and again any time you want to retrain on more live data:

    python train_model.py

Requires: pip install xgboost joblib
"""

import os

import joblib
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

INSTRUCTOR_COLS = ["Midterm_Score", "Assignments_Avg", "Quizzes_Avg", "Participation_Score", "Projects_Score"]
DOCTOR_COLS = ["Attendance (%)", "Study_Hours_per_Week", "Stress_Level (1-10)", "Sleep_Hours_per_Night"]
FEATURES = INSTRUCTOR_COLS + DOCTOR_COLS
TARGET = "Total_Marks_100"

df = pd.read_csv("Final_Target_Students_Performance.csv")

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBRegressor(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    random_state=42,
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print(f"R2:  {r2_score(y_test, pred):.4f}")
print(f"MAE: {mean_absolute_error(y_test, pred):.3f}")

doctor_baseline_means = {col: float(df[col].mean()) for col in DOCTOR_COLS}

artifact = {
    "model": model,
    "feature_order": FEATURES,
    "instructor_cols": INSTRUCTOR_COLS,
    "doctor_cols": DOCTOR_COLS,
    "doctor_baseline_means": doctor_baseline_means,
}

os.makedirs("api/ml", exist_ok=True)
joblib.dump(artifact, "api/ml/performance_model.joblib")

print("Saved model to api/ml/performance_model.joblib")