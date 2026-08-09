# 📄 ResumeIQ-A Resume Feedback Tool

**AI-Powered Resume Analysis with Structured JSON Feedback**

`Python` `Flask` `Groq` `Llama 3.3` `HTML/CSS/JS`

---

## 📌 Overview

**Resume Feedback Tool** is a lightweight, full-stack AI application that gives job seekers instant, structured feedback on their resumes — the kind of feedback you'd normally pay a career coach for.

Instead of returning a vague paragraph of generic advice, the app enforces a **strict structured JSON schema** on the LLM's output, which is then rendered into clean, scannable cards on the frontend: an overall score, strengths, weaknesses, actionable suggestions, and a rewritten professional summary.

The system automatically:

✅ Accepts raw resume text (with an optional target job title)  
✅ Sends a carefully engineered prompt to a Groq-hosted LLM  
✅ Forces the model to return **only valid JSON** in a fixed schema  
✅ Parses and validates the JSON on the backend  
✅ Renders the feedback as structured UI cards in real time  

---

## 🖥️ Application Preview

**Input Panel**
- Target Job Title field (optional) — tailors feedback to a specific role
- Resume Text box — paste any plain-text resume
- One-click "Get Feedback" action

**Feedback Dashboard**
- 🎯 Overall Score (0–100)
- ✍️ Rewritten Professional Summary
- 💪 Strengths
- ⚠️ Weaknesses
- 💡 Actionable Suggestions

---

## 🚀 Key Features

### 🧩 Structured JSON Output
The core "advanced" element of this project. The system prompt forces the LLM to respond with **only** a JSON object matching a fixed schema — no prose, no markdown fences — which the backend safely parses with a regex-based cleanup + `json.loads()` fallback.

| Field | Type | Description |
|---|---|---|
| `overall_score` | integer (0–100) | Overall resume strength |
| `strengths` | list[string] | 3–5 things done well |
| `weaknesses` | list[string] | 3–5 gaps or issues |
| `suggestions` | list[string] | 3–5 concrete fixes |
| `rewritten_summary` | string | Polished 2–3 sentence professional summary |

### 🎯 Role-Aware Feedback
If the user provides a target job title, the prompt instructs the model to tailor both the critique and the rewritten summary toward that specific role — surfacing mismatches between the resume and the job.

### 🛡️ Input Validation & Error Handling
- Rejects resumes that are too short to meaningfully analyze
- Gracefully handles malformed JSON responses from the LLM
- Surfaces clear error messages to the user instead of failing silently

---

## 🏗️ System Workflow

```
User pastes resume + (optional) target role
              │
              ▼
   Flask receives POST /analyze
              │
              ▼
  System prompt + user resume sent to Groq
        (llama-3.3-70b-versatile)
              │
              ▼
   Model returns raw text (strict JSON)
              │
              ▼
   extract_json() cleans & parses response
              │
              ▼
   JSON returned to frontend via API
              │
              ▼
  UI renders score, strengths, weaknesses,
     suggestions & rewritten summary
```

---

## 🧠 Technologies Used

**Backend & AI**
- Python 3.x
- Flask — lightweight web server & API routing
- Groq API — fast LLM inference (`llama-3.3-70b-versatile`)
- python-dotenv — secure local API key management

**Frontend**
- HTML / CSS / vanilla JavaScript (no framework needed)
- Fetch API for async calls to the backend

---

## 📂 Project Structure

```
resume_feedback_app/
│
├── app.py                # Flask backend + Groq API call + JSON parsing
├── templates/
│   └── index.html        # Frontend UI (form + results dashboard)
├── requirements.txt      # Project dependencies
├── .env.example           # Template for your Groq API key
└── README.md
```

---

## ⚙️ Installation

**1. Clone / extract the project**
```bash
cd resume_feedback_app
```

**2. Create a virtual environment**
```bash
python -m venv venv
```

**3. Activate the environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Add your Groq API key**

Rename `.env.example` to `.env` and add your key:
```
GROQ_API_KEY=your-key-here
```
Get a free key at [console.groq.com](https://console.groq.com)

---

## ▶️ Run Application

```bash
python app.py
```

Access the application in your browser at:

**http://127.0.0.1:5000**

---

## 🧪 Test Cases

| # | Scenario | Expected Result |
|---|---|---|
| 1 | Strong resume with metrics ("increased sales 30%") | High score, strong strengths list |
| 2 | Vague resume, duties only, no results | Lower score, flags lack of impact |
| 3 | Resume/role mismatch (e.g. chef → "Software Engineer") | Surfaces the mismatch clearly |
| 4 | Very short/incomplete resume | Triggers input validation error |
| 5 | Poorly formatted resume, no clear sections | Flagged under weaknesses |

---

## 🎯 Future Enhancements

- **RAG Integration:** Feed in an actual job description as retrieval context for hyper-tailored feedback
- **PDF Upload:** Accept `.pdf` / `.docx` resumes directly instead of pasted text
- **Automation:** Auto-email the feedback report to the user
- **Export:** Download feedback as a PDF report
- **History:** Store past analyses for before/after comparison

---

## 👨‍💻 Developer

**Resume Feedback Tool** — built as an AI/ML capstone mini-project combining prompt engineering, API integration, and structured output design.

---

## ⚠️ Disclaimer

This tool is built for educational and self-improvement purposes. Feedback is AI-generated and should be used as a starting point — always have a human review your resume for final submission.
