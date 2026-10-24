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
├── index.html          # Web App for GitHub Pages (Interactive UI)
├── app.py              # Streamlit Web App (Local Python UI)
├── ai_engine.py        # Core AI engine (Gemini 3.8 Flash API integration)
├── cli_demo.py         # Minimal terminal version for testing raw Python logic
├── sample_notes.txt    # Example study notes on AI foundations
├── test_engine.py      # Automated unit test to verify your setup
├── run.bat             # 1-click Windows launcher
└── README.md           # Project documentation and guide
```

---

## 🚀 How to Run the Project

### Option A: Online on GitHub Pages
Visit the live deployed app:
👉 **https://dlsnice.github.io/Dls_Study_Buddy_Ai/**

### Option B: 1-Click Launch (Locally)
Simply double-click the **`run.bat`** file in this folder. It will activate the virtual environment and open your browser automatically at `http://localhost:8501`.

### Option C: From Terminal
```powershell
.\.venv\Scripts\activate
streamlit run app.py
```
