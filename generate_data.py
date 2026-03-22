import pandas as pd
import numpy as np
import random

np.random.seed(42)

n = 250  # number of students

branches = ["CSE", "ECE", "IT", "EEE", "MECH"]
skills_list = ["Python", "Java", "ML", "Web Dev", "None"]
companies = ["TCS", "Infosys", "Wipro", "Google", "Amazon", "Microsoft"]

data = []

for i in range(n):
    student_id = i + 1

    branch = random.choice(branches)

    # CGPA distribution (realistic)
    cgpa = round(np.random.normal(7.0, 1.0), 2)
    cgpa = max(5.0, min(9.8, cgpa))  # keep within range

    # Skill logic based on CGPA
    if cgpa > 8:
        skills = random.choice(["Python", "ML", "Web Dev"])
    elif cgpa > 6:
        skills = random.choice(["Java", "Python", "None"])
    else:
        skills = "None"

    # Internship probability depends on CGPA
    internship = np.random.choice([0, 1], p=[0.7, 0.3] if cgpa < 7 else [0.4, 0.6])

    # Aptitude score
    aptitude = int(np.random.normal(65, 15))
    aptitude = max(30, min(100, aptitude))

    # Placement logic (VERY IMPORTANT)
    placed = 0
    salary = 0
    company = "None"

    if cgpa > 6.5 and aptitude > 55:
        if skills != "None":
            chance = 0.6
            if internship == 1:
                chance += 0.2

            if random.random() < chance:
                placed = 1
                company = random.choice(companies)

                # Salary depends on skills
                if skills == "ML":
                    salary = np.random.randint(800000, 2000000)
                elif skills == "Python":
                    salary = np.random.randint(500000, 1500000)
                elif skills == "Web Dev":
                    salary = np.random.randint(400000, 1200000)
                else:
                    salary = np.random.randint(300000, 800000)

    data.append([
        student_id, branch, cgpa, skills,
        internship, aptitude, company, salary, placed
    ])

columns = [
    "Student_ID", "Branch", "CGPA", "Skills",
    "Internship", "Aptitude", "Company", "Salary", "Placed"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("data/placement_data.csv", index=False)

print("✅ Dataset created successfully!")