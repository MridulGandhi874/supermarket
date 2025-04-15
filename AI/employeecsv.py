import pandas as pd
import numpy as np

# Settings
np.random.seed(42)
num_candidates = 5000
education_levels = ['High School', 'Bachelor’s', 'Master’s', 'PhD']
education_weights = [0.2, 0.5, 0.25, 0.05]

data = []

for candidate_id in range(1, num_candidates + 1):
    # YearsExperience
    experience_bucket = np.random.choice(['entry', 'mid', 'senior'], p=[0.6, 0.3, 0.1])
    if experience_bucket == 'entry':
        years_experience = np.random.randint(0, 6)
    elif experience_bucket == 'mid':
        years_experience = np.random.randint(5, 11)
    else:
        years_experience = np.random.randint(10, 21)

    # EducationLevel
    education_level = np.random.choice(education_levels, p=education_weights)

    # SkillScore
    skill_mean = 70
    if education_level in ['Master’s', 'PhD']:
        skill_mean += 5
    skill_score = round(np.clip(np.random.normal(skill_mean, 10), 0, 100), 2)

    # Certifications
    certifications = np.random.choice([0, 1, 2, 3, 4, 5], p=[0.5, 0.3, 0.15, 0.03, 0.01, 0.01])

    # ShouldHire
    should_hire = 1 if (years_experience >= 5 or skill_score >= 80 or
                        (education_level in ['Master’s', 'PhD'] and certifications >= 2)) else 0
    if np.random.random() < 0.1:
        should_hire = 1 - should_hire

    data.append([candidate_id, years_experience, education_level, skill_score, certifications, should_hire])

# Create DataFrame and save
df = pd.DataFrame(data, columns=['CandidateID', 'YearsExperience', 'EducationLevel', 'SkillScore',
                                 'Certifications', 'ShouldHire'])
df.to_csv('employee_cv.csv', index=False)
print("Dataset saved as employee_cv.csv")