"""
Resume Feedback Tool
---------------------
A small AI-powered mini app that gives structured feedback on a resume.

Core flow:
  INPUT  -> user pastes their resume text (and optionally a target job title)
  OUTPUT -> AI returns structured JSON feedback:
              - overall_score (0-100)
              - strengths (list)
              - weaknesses (list)
              - suggestions (list)
              - rewritten_summary (a polished 2-3 sentence professional summary)

Advanced element used: STRUCTURED JSON OUTPUT (Week 4-5 requirement).

Setup:
  1. pip install -r requirements.txt
  2. Set your Groq API key as an environment variable:
       export GROQ_API_KEY="your-key-here"
  3. Run:  python app.py
  4. Open http://127.0.0.1:5000 in your browser
"""

import os
import json
import re
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # reads GROQ_API_KEY from a local .env file, if present

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"  # any current Groq-hosted model works

SYSTEM_PROMPT = """You are an expert resume reviewer and career coach with 15 years of experience in technical and non-technical hiring.

You will be given a resume (plain text) and optionally a target job title.

Your job is to analyze the resume and return ONLY a valid JSON object (no markdown fences, no extra commentary) with EXACTLY this shape:

{
  "overall_score": <integer 0-100>,
  "strengths": [<3-5 short strings>],
  "weaknesses": [<3-5 short strings>],
  "suggestions": [<3-5 short, actionable strings>],
  "rewritten_summary": "<a polished 2-3 sentence professional summary the user could paste at the top of their resume>"
}

Rules:
- Be honest and specific, not generic. Reference actual content from the resume where possible.
- If a target job title is given, tailor the feedback and rewritten_summary toward that role.
- overall_score should reflect clarity, impact (use of metrics/results), formatting cues, and relevance.
- Return ONLY the JSON object. No preamble, no explanation, no markdown code fences.
"""


def extract_json(text: str) -> dict:
    """Strip markdown fences if present and parse JSON safely."""
    cleaned = re.sub(r"^```json\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
    cleaned = cleaned.strip("` \n")
    return json.loads(cleaned)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    resume_text = (data.get("resume_text") or "").strip()
    target_role = (data.get("target_role") or "").strip()

    if not resume_text or len(resume_text) < 30:
        return jsonify({"error": "Please paste a fuller resume (at least a few lines)."}), 400

    user_message = f"Target job title: {target_role or 'Not specified'}\n\nResume:\n{resume_text}"

    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=1000,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        raw_text = response.choices[0].message.content
        parsed = extract_json(raw_text)
        return jsonify(parsed)

    except json.JSONDecodeError:
        return jsonify({"error": "The AI response wasn't valid JSON. Try again."}), 502
    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)