# 🧠 StudyBuddy AI – Intelligent Learning & Research Assistant

A complete, beginner-friendly AI project designed to help you learn modern AI engineering by doing.

---

## 🌟 Why this is the best AI project for beginners

This project touches all core pillars of modern AI application development without overwhelming you with complex math:

1. **System Prompting & Personas:** Learn how instructions shape AI behavior (Tutor, Code Mentor, ELI5 Explainer).
2. **Hyperparameter Tuning:** See firsthand how `temperature` changes model creativity vs. determinism.
3. **Structured Outputs:** Extract reliable JSON data from an LLM to build interactive quizzes.
4. **Document Grounding (Mini-RAG):** Feed text notes or articles into the prompt so the AI answers accurately without hallucinations.
5. **Interactive Web Interface:** A sleek UI built in pure Python using **Streamlit**.
6. **Built-in Demo Mode:** Works out of the box with realistic mock responses even if you don't have an API key yet!

---

## 📂 Project Architecture

```
ai_study_assistant/
│
├── app.py              # Streamlit Web App (Interactive UI with tabs & cards)
├── ai_engine.py        # Core AI engine (API calls, structured JSON, fallback logic)
├── cli_demo.py         # Minimal terminal version for testing raw Python logic
├── sample_notes.txt    # Example study notes on AI foundations
├── test_engine.py      # Automated unit test to verify your setup
├── run.bat             # 1-click Windows launcher
└── README.md           # Project documentation and guide
```

---

## 🚀 How to Run the Project

### Option A: 1-Click Launch (Easiest)
Simply double-click the **`run.bat`** file in this folder. It will activate the virtual environment and open your browser automatically at `http://localhost:8501`.

### Option B: From the Terminal / PowerShell
1. Open PowerShell or Command Prompt in this folder:
   ```powershell
   cd "C:\Users\Nice Interactive\.gemini\antigravity\scratch\ai_study_assistant"
   ```
2. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\activate
   ```
3. Run the Streamlit web app:
   ```powershell
   streamlit run app.py
   ```

### Option C: Minimal Terminal CLI (No Web Browser)
If you just want to see how AI chat works in raw Python:
```powershell
.\.venv\Scripts\activate
python cli_demo.py
```

---

## 🔑 (Optional) Connecting a Free Google Gemini API Key

The app works right away in **Demo Mode**, but connecting a live model makes it truly intelligent!

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and sign in.
2. Click **Create API Key** (Google provides free access with generous rate limits).
3. Copy your key, launch the app, and paste it into the **Google Gemini API Key** field in the left sidebar.
4. The status badge will switch to **🟢 Live API Mode**!

---

## 💡 Key AI Concepts You Will Learn from the Code

### 1. Temperature (`ai_engine.py`)
- `temperature = 0.0`: The model chooses the most probable tokens every time. Perfect for code, math, and factual document Q&A.
- `temperature = 0.7 - 1.0`: The model explores varied vocabulary. Perfect for creative writing and brainstorming.

### 2. Structured JSON Output (`generate_quiz` in `ai_engine.py`)
Instead of receiving conversational text, we tell the model:
```json
[
  {
    "question": "What is a token?",
    "options": ["A", "B", "C", "D"],
    "correct_index": 0,
    "explanation": "..."
  }
]
```
With `response_mime_type="application/json"`, the model guarantees a valid JSON output, which Python parses directly into interactive UI components!

### 3. Grounding / Mini-RAG (`analyze_document` in `ai_engine.py`)
Language models can hallucinate facts. By injecting source notes into the prompt between separators (`---`), we force the model to answer based strictly on verified material.

---

## 🛠️ Challenges to Level Up Your Skills
Try modifying the code to add your own features:
1. **Flashcard Mode:** Add a button in `app.py` that generates 5 two-sided study flashcards.
2. **Export to File:** Add a button to save the generated quiz or summary to a `.txt` or `.md` file on your computer.
3. **Voice Input/Output:** Experiment with Python's `pyttsx3` library to have the AI tutor speak answers out loud!
