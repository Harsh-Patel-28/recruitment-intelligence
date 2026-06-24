from google import genai
import json
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

print("KEY FOUND:", os.getenv("GEMINI_API_KEY") is not None)  # sanity check, remove later

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_resume_info(resume_text: str) -> dict:

    prompt = f"""
    You are a resume parser. Extract information from this resume text.

    Return ONLY a JSON object, no extra text, no markdown, just pure JSON like this:
    {{
        "name": "candidate name",
        "skills": ["skill1", "skill2"],
        "experience_years": 2,
        "education": "degree and college name",
        "summary": "one line about the candidate"
    }}

    Resume text:
    --------------
    {resume_text}
    --------------
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    clean = response.text.strip().replace("```json", "").replace("```", "")

    return json.loads(clean)


def score_resume(resume_info: dict, job_description: str) -> dict:

    prompt = f"""
    You are an expert technical recruiter. Compare this candidate's resume 
    information against the job description and evaluate fit.

    Candidate Resume Info:
    {json.dumps(resume_info)}

    Job Description:
    --------------
    {job_description}
    --------------

    Return ONLY a JSON object, no extra text, no markdown, in this exact format:
    {{
        "score": 85,
        "matched_skills": ["skill1", "skill2"],
        "missing_skills": ["skill3", "skill4"],
        "reasoning": "2-3 sentences explaining the score"
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    clean = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(clean)

def generate_interview_questions(resume_info: dict, score_result: dict) -> dict:

    prompt = f"""
    You are a senior technical interviewer. Based on the candidate's resume 
    and their skill gap analysis, generate 5 targeted interview questions.

    Candidate Info:
    {json.dumps(resume_info)}

    Skill Match Analysis:
    {json.dumps(score_result)}

    Generate a mix of:
    - 2 questions about their matched/strong skills (to verify depth)
    - 2 questions probing their missing skills (to test if they can learn fast or have hidden exposure)
    - 1 behavioral/project-based question using their actual projects/experience

    Return ONLY a JSON object, no extra text, no markdown, in this exact format:
    {{
        "questions": [
            {{"type": "technical", "question": "..."}},
            {{"type": "skill_gap", "question": "..."}},
            {{"type": "behavioral", "question": "..."}}
        ]
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    clean = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(clean)

if __name__ == "__main__":
    test_text = "John Doe, Python developer, 2 years experience, knows FastAPI, ML. B.Tech CSE from GTU."
    resume_info = extract_resume_info(test_text)
    print("PARSED:", resume_info)

    job_desc = "Looking for a backend developer skilled in Python, FastAPI, and SQL databases."
    score_result = score_resume(resume_info, job_desc)
    print("SCORE:", score_result)

    questions = generate_interview_questions(resume_info, score_result)
    print("QUESTIONS:", questions)