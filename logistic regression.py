import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


df = pd.read_csv("Cleaned_Students_Performance.csv")


df["Passed"] = (df["Total_Score"] >= 60).astype(int)


X = df[["Study_Hours_per_Week", "Attendance (%)", "Assignments_Avg", "Quizzes_Avg"]]
y = df["Passed"] 


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)



classifier = LogisticRegression()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
struggling_student = [[5, 50.0, 40.0, 45.0]]
pass_prediction = classifier.predict(struggling_student)[0]
pass_probability = classifier.predict_proba(struggling_student)[0][1]

print(
    f"Prediction: {'Pass (1)' if pass_prediction == 1 else 'Fail (0)'} "
    f"(Pass Probability: {pass_probability * 100:.2f}%)"
)