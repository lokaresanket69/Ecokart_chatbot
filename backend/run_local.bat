@echo off
REM Activate your virtual environment if needed
REM call venv\Scripts\activate
cd /d %~dp0
set FLASK_APP=app.py
set FLASK_ENV=development
flask run --host=127.0.0.1 --port=5000 