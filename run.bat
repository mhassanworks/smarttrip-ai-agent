@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul || (echo Python 3 was not found. & exit /b 1)
python -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)" || (echo Python 3.11+ is required. & exit /b 1)
if not exist ".venv" python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address localhost --server.port 8501 --server.headless true
