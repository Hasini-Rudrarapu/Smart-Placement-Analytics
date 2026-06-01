SKILLS = [
    "python",
    "java",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "machine learning",
    "deep learning",
    "data analytics",
    "data visualization",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "mongodb",
    "aws",
    "git",
    "flask",
    "streamlit",
    "postgresql",
    "mysql",
    "firebase"
]

def extract_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return found