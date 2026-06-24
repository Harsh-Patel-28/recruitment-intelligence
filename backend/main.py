from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from parser import extract_text_from_pdf
from gemini_service import extract_resume_info, score_resume, generate_interview_questions

app = FastAPI()

# Allow frontend (any origin, for development) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # "*" = allow any origin (fine for local dev, not production)
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Recruitment Intelligence API is running!"}

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    pdf_bytes = await resume.read()
    resume_text = extract_text_from_pdf(pdf_bytes)
    parsed_info = extract_resume_info(resume_text)
    score_result = score_resume(parsed_info, job_description)
    questions = generate_interview_questions(parsed_info, score_result)

    return {
        "filename": resume.filename,
        "parsed_resume": parsed_info,
        "score_result": score_result,
        "interview_questions": questions
    }