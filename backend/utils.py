import pdfplumber
from sarvamai import SarvamAI
from dotenv import load_dotenv
import os
from collections import Counter

# Load .env located next to this file (backend/.env) or fall back to other locations
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    # fallback to .env in cwd or parent directories
    load_dotenv()

# Read API key from environment (or from api_key.txt files as a last resort)
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
if not SARVAM_API_KEY:
    # try parent package .env
    parent_env = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(parent_env):
        load_dotenv(parent_env)
        SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

if not SARVAM_API_KEY:
    raise RuntimeError(
        "SARVAM_API_KEY not found. Add it to backend/.env, set environment variable SARVAM_API_KEY, or place it in api_key.txt."
    )

# Init client
client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

# Extract text from PDF
def extract_text_from_pdf(file) -> str:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

# Fallback: Top 5 most frequent words
def get_top_words(text: str):
    words = [w.lower() for w in text.split() if w.isalpha()]
    counter = Counter(words)
    # return list of words instead of raw string
    return [word for word, _ in counter.most_common(5)]

# Placeholder for AI summarization
import json
import re

def generate_summary(text: str):
    try:
        system_instructions = (
            "You are an ATS-style resume evaluator. "
            "Return ONLY a single valid JSON object (no markdown, no backticks, no commentary, no <think>). "
            "All scores must be integers 0-100. verdict must be exactly one of: Strong, Average, Weak."
        )

        # Keep the user prompt compact to reduce token waste and avoid finish_reason='length'.
        prompt = f"""
Analyze the RESUME TEXT and produce a JSON with this exact schema:
{{
  "scores": {{
    "relevance": 0,
    "keyword_optimization": 0,
    "formatting_presentation": 0,
    "achievements_qualifications": 0,
    "brevity_clarity": 0,
    "final_score": 0
  }},
  "summary": "",
  "technical_skills": [],
  "work_experience": [],
  "key_projects": [],
  "academic_achievements": [],
  "recommendations": [],
  "verdict": "Strong"
}}

Scoring rules:
- Each category score is 0-100.
- final_score is 0-100 where Relevance and Achievements have 2x weight vs others.

RESUME TEXT:
{text}
""".strip()

        def _call(messages, *, temperature: float):
            return client.chat.completions(
                messages=messages,
                max_tokens=1200,
                temperature=temperature,
            )

        def _parse_json(raw_output: str):
            raw_output = (raw_output or "").strip()

            # 1) Try parsing as-is
            try:
                return json.loads(raw_output)
            except Exception:
                pass

            # 2) Parse between first '{' and last '}'
            start = raw_output.find("{")
            end = raw_output.rfind("}")
            if start == -1 or end == -1 or end <= start:
                return None

            json_str = raw_output[start : end + 1]
            return json.loads(json_str)

        messages = [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": prompt},
        ]

        response = _call(messages, temperature=0.2)
        raw_output = response.choices[0].message.content
        finish_reason = getattr(response.choices[0], "finish_reason", None)
        if finish_reason == "length":
            print("Sarvam AI Warning: response truncated (finish_reason=length)")

        parsed = _parse_json(raw_output)
        if parsed is not None:
            return parsed

        # One retry: some models ignore constraints on first try. This keeps the app robust.
        retry_messages = [
            {
                "role": "system",
                "content": system_instructions
                + " You must output ONLY JSON. Do NOT include any explanation.",
            },
            {"role": "user", "content": prompt},
        ]
        retry_response = _call(retry_messages, temperature=0.0)
        retry_raw = retry_response.choices[0].message.content

        parsed = _parse_json(retry_raw)
        if parsed is None:
            snippet = ((retry_raw or "")[:500]).replace("\n", " ")
            raise ValueError(
                f"No JSON found in AI response after retry. Output starts with: {snippet!r}"
            )

        return parsed

    except Exception as e:
        print("Sarvam AI Error:", str(e))
        return None
