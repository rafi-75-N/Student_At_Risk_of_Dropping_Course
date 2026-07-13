import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("Students Performance Dataset.csv")


column1_academic = ['Midterm_Score', 'Assignments_Avg', 'Quizzes_Avg', 'Participation_Score', 'Projects_Score']
routine_features = ['Attendance (%)', 'Study_Hours_per_Week', 'Stress_Level (1-10)', 'Sleep_Hours_per_Night']


for col in column1_academic + routine_features:
  
    df[col] = pd.to_numeric(df[col].astype(str).str.replace('%', '').str.strip(), errors='coerce')


df[column1_academic] = df[column1_academic].fillna(0)
df[routine_features] = df[routine_features].fillna(0)


df['Total_Academic_Marks'] = df[column1_academic].sum(axis=1)


attendance_weight = (df['Attendance (%)'] / 100) * 25
study_weight = (df['Study_Hours_per_Week'] / 30) * 25
stress_weight = ((10 - df['Stress_Level (1-10)']) / 9) * 25  
sleep_weight = (df['Sleep_Hours_per_Night'] / 9) * 25

df['Discipline_Index'] = attendance_weight + study_weight + stress_weight + sleep_weight


def evaluate_routine(score):
    if score >= 65:
        return 'Optimal'
    elif score >= 45:
        return 'Balanced'
    else:
        return 'Concerning'

df['Routine_Status'] = df['Discipline_Index'].apply(evaluate_routine)


fig, axes = plt.subplots(2, 2, figsize=(14, 10))


sns.lineplot(data=df, x=pd.qcut(df['Attendance (%)'], q=10, duplicates='drop').astype(str), 
             y='Total_Academic_Marks', ax=axes[0, 0], marker='o', color='royalblue', errorbar=None)
axes[0, 0].set_title('Attendance vs Total Academic Marks')
axes[0, 0].set_xlabel('Attendance Percentile Tiers')
axes[0, 0].set_ylabel('Avg Total Academic Marks')
axes[0, 0].tick_params(axis='x', rotation=15)


sns.lineplot(data=df, x=df['Study_Hours_per_Week'].round(), 
             y='Total_Academic_Marks', ax=axes[0, 1], marker='o', color='forestgreen', errorbar=None)
axes[0, 1].set_title('Weekly Study Hours vs Total Academic Marks')
axes[0, 1].set_xlabel('Study Hours')
axes[0, 1].set_ylabel('Avg Total Academic Marks')


sns.lineplot(data=df, x='Stress_Level (1-10)', 
             y='Total_Academic_Marks', ax=axes[1, 0], marker='o', color='crimson', errorbar=None)
axes[1, 0].set_title('Stress Level vs Total Academic Marks')
axes[1, 0].set_xlabel('Stress Level (1 to 10)')
axes[1, 0].set_ylabel('Avg Total Academic Marks')


sns.lineplot(data=df, x=df['Sleep_Hours_per_Night'].round(), 
             y='Total_Academic_Marks', ax=axes[1, 1], marker='o', color='darkorchid', errorbar=None)
axes[1, 1].set_title('Nightly Sleep Hours vs Total Academic Marks')
axes[1, 1].set_xlabel('Sleep Hours')
axes[1, 1].set_ylabel('Avg Total Academic Marks')

plt.tight_layout()
plt.savefig('routine_correlations.png')
plt.show()


df.to_csv("Cleaned_Students_Performance.csv", index=False)



print(df[column1_academic + routine_features].to_string())
