import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


df = pd.read_csv("Cleaned_Students_Performance.csv")


X =  df[["Study_Hours_per_Week", "Attendance (%)", "Assignments_Avg", "Quizzes_Avg"]]
y =             df["Total_Score"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)  

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R2 Score: {r2:.2f}")
new_student = [[20, 85.0, 75.0, 80.0]]
predicted_score = model.predict(new_student)
print(f"Predicted Total Score for new student: {predicted_score[0]:.2f}")