# 📄 AI-Doc-Insight-Tool  

AI-Doc-Insight-Tool is a full-stack application that allows users to upload documents (e.g., resumes) and instantly generate AI-powered insights and summaries. The tool also provides search, filtering, and PDF report downloads with clean formatting. 

## ✨ Features
- 🚀 **Resume Upload**: Upload PDF resumes through a clean React UI.  
- 🤖 **AI-Powered Insights**: Uses Sarvam AI to generate summaries of resumes.  
- 🛡 **Fallback Mechanism**: If AI is unavailable, returns the top 5 frequent words.  
- 📊 **Insights Viewer**: Displays results in a structured format with headings and a verdict pill.  
- 🗂 **History Tab**: Browse past uploads with search & sorting support.  
- 📑 **PDF Report Download**: Generate well-formatted PDF reports with insights.
- 🔍 Search and filter documents by filename or keywords.
- 🎨 Modern UI built with React + TailwindCSS.
- 🗄 Persistent document storage with SQLite + SQLAlchemy.
- ⚡ Backend powered by FastAPI.

## ⚙️ Tech Stack
- Frontend → React, TailwindCSS
- Backend → FastAPI, SQLAlchemy
- Database → SQLite (default, can be swapped with PostgreSQL/MySQL)
- AI Layer → Sarvam AI API (summarization)
- PDF Reports → ReportLab
---

## 🔧 Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Mayur-143/AI-Doc-Insight-Tool.git
cd AI-Doc-Insight-Tool
```
### 2️⃣ Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux
cd ../
pip install -r requirements.txt
```
Create a .env file inside the backend/ folder:
```bash
SARVAM_API_KEY=your_api_key_here
```
Run Backend (from root directory): 
```bash
uvicorn main:app --reload
```
Backend will run at → http://127.0.0.1:8000
### Database
- By default, SQLite is used. The DB file is automatically created on first run.
- Can be swapped with PostgreSQL/MySQL by updating database.py.

### 3️⃣ Frontend Setup (React + Tailwind)
```bash
cd frontend
npm install
npm start
```
Frontend will run at → http://localhost:3000

## 🖼 Sample Workflow
- Upload a resume PDF.
- Backend extracts text → calls Sarvam AI API for summarization.
- Insights are stored in the database.
- Frontend displays AI-generated insights.
- User can search, filter, and download the insights report (PDF).

## 📂 Example API Endpoints
- POST /upload-resume → Uploads a PDF and generates insights.
- GET /insights → Fetch all uploaded documents with insights.
- GET /insights?doc_id=<id> → Fetch insights for a single document.
- GET /download-report/{doc_id} → Download formatted PDF report.

## 🌟 Future Enhancements
- User login/logout with secure sessions.
- Support for multiple document formats (DOCX, TXT).
- Enhanced AI insights (job fit, ATS score, recommendations).
- Deployment via Docker + CI/CD pipeline.
