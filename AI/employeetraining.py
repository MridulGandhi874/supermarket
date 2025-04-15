import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Define valid education levels
education_levels = ['High School', 'Bachelor’s', 'Master’s', 'PhD']

# Load the dataset
data = pd.read_csv('../datasets/employee_cv.csv')

# Step 1: Prepare features and target
X = data[['YearsExperience', 'EducationLevel', 'SkillScore', 'Certifications']]
y = data['ShouldHire']

# Step 2: Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), ['EducationLevel']),
        ('num', 'passthrough', ['YearsExperience', 'SkillScore', 'Certifications'])
    ])

# Step 3: Create and train model pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])
model.fit(X, y)

# Step 4: Calculate accuracy
accuracy = model.score(X, y)

# Step 5: Save the model
model_filename = '../models/employeehire/hire_model.joblib'
joblib.dump(model, model_filename)

# Step 6: Print model details
feature_names = (model.named_steps['preprocessor']
                 .named_transformers_['cat']
                 .get_feature_names_out(['EducationLevel'])
                 .tolist() + ['YearsExperience', 'SkillScore', 'Certifications'])
importances = model.named_steps['classifier'].feature_importances_
print("\nHiring Prediction Model:")
for name, importance in zip(feature_names, importances):
    print(f"Feature Importance: {name} = {importance:.4f}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Model saved as: {model_filename}")


# Step 7: Prediction function
def predict_hire(years_experience, education_level, skill_score, certifications):
    """
    Predict if a candidate should be hired based on CV details.

    Parameters:
    - years_experience (int): Years of professional experience
    - education_level (str): Highest degree (High School, Bachelor’s, Master’s, PhD)
    - skill_score (float): Skill score (0–100)
    - certifications (int): Number of certifications

    Returns:
    - Prediction and recommendation (str)
    """
    # Validate inputs
    if not isinstance(years_experience, (int, float)) or years_experience < 0:
        return f"Error: YearsExperience must be a non-negative number, got {years_experience}"
    if education_level not in education_levels:
        return f"Error: Invalid EducationLevel. Choose from {education_levels}"
    if not isinstance(skill_score, (int, float)) or skill_score < 0 or skill_score > 100:
        return f"Error: SkillScore must be between 0 and 100, got {skill_score}"
    if not isinstance(certifications, int) or certifications < 0:
        return f"Error: Certifications must be a non-negative integer, got {certifications}"

    # Create input DataFrame
    X_pred = pd.DataFrame({
        'YearsExperience': [years_experience],
        'EducationLevel': [education_level],
        'SkillScore': [skill_score],
        'Certifications': [certifications]
    })

    # Predict
    should_hire = model.predict(X_pred)[0]
    recommendation = "Hire this candidate." if should_hire else "Do not hire this candidate."
    return (f"Prediction for candidate (Experience={years_experience} years, Education={education_level}, "
            f"SkillScore={skill_score}, Certifications={certifications}): "
            f"{'Hire' if should_hire else 'Not Hire'}. {recommendation}")


# Step 8: Example usage with user input
def get_user_prediction():
    try:
        years_experience = int(input("Enter years of experience: "))
        education_level = input("Enter education level (High School, Bachelor’s, Master’s, PhD): ")
        skill_score = float(input("Enter skill score (0–100): "))
        certifications = int(input("Enter number of certifications: "))

        result = predict_hire(years_experience, education_level, skill_score, certifications)
        print(result)
    except ValueError:
        print("Error: Please enter valid numeric values where required")


# Run example predictions
print("\nRunning example predictions:")
print(predict_hire(7, 'Master’s', 85, 2))
print(predict_hire(1, 'High School', 60, 0))
print(predict_hire(5, 'Bachelor’s', 75, 1))

# Uncomment to enable interactive input
# get_user_prediction()