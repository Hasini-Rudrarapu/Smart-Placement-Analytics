from openai import OpenAI
import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def review_resume(resume_text):

    prompt = f"""
    Analyze this resume.

    Give:

    1. Strengths
    2. Weaknesses
    3. Improvement Suggestions

    Resume:
    {resume_text[:3000]}
    """

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        max_tokens=500,
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    return response.choices[0].message.content