# 🧠 Recruitment Intelligence

An AI-powered recruitment pipeline that parses resumes, scores them against a job description, and auto-generates targeted interview questions — built to mimic how a human recruiter screens candidates, but in seconds.

## 🎯 What it does

1. **Upload a resume (PDF)** + paste a job description
2. **AI extracts structured candidate data** — skills, education, experience
3. **AI scores the match (0-100)** with reasoning, plus matched/missing skills
4. **AI generates 5 targeted interview questions** based on the candidate's actual strengths and gaps

## 🏗️ How it works

Resume PDF ──▶ Text Extraction ──▶ Gemini AI Parsing ──▶ Structured JSON

│

Job Description ─────────────────────────┤

▼

Match Scoring (Gemini)

│

▼

Interview Question Generation (Gemini)

│

▼

Results shown in UI

## 🛠️ Tech Stack

**Backend**
- Python, FastAPI — REST API
- PyMuPDF — PDF text extraction
- Google Gemini API (`gemini-2.5-flash`) — resume parsing, scoring, question generation

**Frontend**
- HTML, CSS, vanilla JavaScript
- `fetch()` for API calls, drag-and-drop file upload

## 📂 Project Structure

recruitment-intelligence/

├── backend/

│   ├── main.py              # FastAPI routes

│   ├── parser.py            # PDF → text extraction

│   ├── gemini_service.py    # All AI logic (parse, score, generate questions)

│   └── requirements.txt

├── frontend/

│   ├── index.html

│   ├── style.css

│   └── script.js

└── README.md

## 🚀 Running it locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Add your Gemini API key to a .env file:
# GEMINI_API_KEY=your_key_here

uvicorn main:app --reload
```

### Frontend
Just open `frontend/index.html` in your browser (server must be running on `localhost:8000`).

## 🔮 Future Improvements

- Batch upload — rank multiple candidates against one job description
- Deploy live (Render + Netlify)
- Support DOCX resumes, not just PDF

## 👤 Author

Built by Patel Harshkumar — B.Tech CSE (AIML), Parul Univercity