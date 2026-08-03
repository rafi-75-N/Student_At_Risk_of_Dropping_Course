import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("Cleaned_Students_Performance.csv")

df['Instructor_Marks_75'] = (
    df['Midterm_Score'] * 0.15 +
    df['Assignments_Avg'] * 0.15 +
    df['Quizzes_Avg'] * 0.10 +
    df['Participation_Score'] * 0.05 +
    df['Projects_Score'] * 0.30
)

df['Doctor_Marks_25'] = df['Discipline_Index'] * 0.25

df['Total_Marks_100'] = df['Instructor_Marks_75'] + df['Doctor_Marks_25']


def get_risk_tier(score):
    if score >= 75:
        return 'No Risk'
    elif score >= 60:
        return 'Medium Risk'
    else:
        return 'High Risk'

def get_target_y(score):
    if score >= 75:
        return 2
    elif score >= 60:
        return 1
    else:
        return 0

df['Final_Risk_Level'] = df['Total_Marks_100'].apply(get_risk_tier)
df['y'] = df['Total_Marks_100'].apply(get_target_y)

features = [
    'Midterm_Score', 'Assignments_Avg', 'Quizzes_Avg', 
    'Participation_Score', 'Projects_Score', 'Attendance (%)', 
    'Study_Hours_per_Week', 'Stress_Level (1-10)', 'Sleep_Hours_per_Night'
]

matrix = df[features].to_numpy()
peer_ids = []

for i in range(len(df)):
    current_student = matrix[i]
    
    distances = np.linalg.norm(matrix - current_student, axis=1)
    
    distances[i] = np.inf
    
    closest_index = np.argmin(distances)
    
    peer_ids.append(df.loc[closest_index, 'Student_ID'])

df['Closest_Historical_Peer_ID'] = peer_ids


print("Risk Label Distribution Summary:")
print(df['Final_Risk_Level'].value_counts())
print("\nNumerical Target (y) Distribution Summary:")
print(df['y'].value_counts())

plt.figure(figsize=(8, 5))
sns.countplot(
    data=df, 
    x='Final_Risk_Level', 
    order=['No Risk', 'Medium Risk', 'High Risk'], 
    palette='Set2'
)

plt.title('Distribution of Student Performance Risk Tiers', fontsize=12, fontweight='bold')
plt.xlabel('Assigned Risk Category')
plt.ylabel('Student Count')
plt.tight_layout()


plt.savefig('final_risk_distribution.png')

df.to_csv("Final_Target_Students_Performance.csv", index=False)
print("Saved clean file: 'Final_Target_Students_Performance.csv'")