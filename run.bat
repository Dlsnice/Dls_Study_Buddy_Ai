@echo off
title StudyBuddy AI Launcher
echo ====================================================
echo Starting StudyBuddy AI Web App...
echo ====================================================
cd /d "%~dp0"
call .venv\Scripts\activate.bat
streamlit run app.py
pause
