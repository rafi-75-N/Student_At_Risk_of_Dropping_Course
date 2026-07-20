import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# 1. READ CLEANED DATASET FROM TASK 1
# ==============================================================================
df = pd.read_csv("Cleaned_Students_Performance.csv")

# ==============================================================================
# 2. CALCULATE COLUMN 1 (INSTRUCTOR MARKS OUT OF 75)
# ==============================================================================
# Apply the exact mathematical weights from the curriculum design
df['Instructor_Marks_75'] = (
    df['Midterm_Score'] * 0.15 +
    df['Assignments_Avg'] * 0.15 +
    df['Quizzes_Avg'] * 0.10 +
    df['Participation_Score'] * 0.05 +
    df['Projects_Score'] * 0.30
)

# ==============================================================================
# 3. CALCULATE COLUMN 2 (DOCTOR ASSESSMENT MARKS OUT OF 25)
# ==============================================================================
# Scale the 0-100 Discipline Index down to account for 25% of the total score
df['Doctor_Marks_25'] = df['Discipline_Index'] * 0.25

# ==============================================================================
# 4. FUSION: UNIFIED TOTAL MARKS (OUT OF 100)
# ==============================================================================
# Sum Column 1 and Column 2 to produce the final 100-point performance metric
df['Total_Marks_100'] = df['Instructor_Marks_75'] + df['Doctor_Marks_25']

# ==============================================================================
# 5. ASSIGN RISK TIERS AND TARGET VARIABLE (y)
# ==============================================================================
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

# Apply the logical functions across the columns
df['Final_Risk_Level'] = df['Total_Marks_100'].apply(get_risk_tier)
df['y'] = df['Total_Marks_100'].apply(get_target_y)

# ==============================================================================
# 6. HISTORICAL SIMILARITY ENGINE (NUMPY DISTANCE VECTOR VECTORIZATION)
# ==============================================================================
# Features used to find the closest matching student profile
features = [
    'Midterm_Score', 'Assignments_Avg', 'Quizzes_Avg', 
    'Participation_Score', 'Projects_Score', 'Attendance (%)', 
    'Study_Hours_per_Week', 'Stress_Level (1-10)', 'Sleep_Hours_per_Night'
]

# Convert features to a clean NumPy matrix for mathematical distance operations
matrix = df[features].to_numpy()
peer_ids = []

# Loop through each student to find their historical matching row
for i in range(len(df)):
    current_student = matrix[i]
    
    # Calculate Euclidean distance vectors using NumPy
    distances = np.linalg.norm(matrix - current_student, axis=1)
    
    # Prevent the student from matching with themselves by setting their own distance to infinity
    distances[i] = np.inf
    
    # Find the index of the closest historical match
    closest_index = np.argmin(distances)
    
    # Grab the Student ID of that closest peer profile
    peer_ids.append(df.loc[closest_index, 'Student_ID'])

df['Closest_Historical_Peer_ID'] = peer_ids

# ==============================================================================
# 7. CONSOLE VERIFICATION REPORT
# ==============================================================================
print("============================================================")
print("             TARGET ENGINEERING PIPELINE COMPLETE")
print("============================================================")
print("Risk Label Distribution Summary:")
print(df['Final_Risk_Level'].value_counts())
print("\nNumerical Target (y) Distribution Summary:")
print(df['y'].value_counts())
print("============================================================")

# ==============================================================================
# 8. DASHBOARD VISUALIZATION USING MATPLOTLIB & SEABORN
# ==============================================================================
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

# Save dashboard chart asset
plt.savefig('final_risk_distribution.png')

# ==============================================================================
# 9. EXPORT DATASET FOR MACHINE LEARNING TRAINING
# ==============================================================================
df.to_csv("Final_Target_Students_Performance.csv", index=False)
print("Saved clean file: 'Final_Target_Students_Performance.csv'")