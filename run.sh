#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python 3 was not found. Install Python 3.11+ and retry."
  exit 1
fi
"$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)' || {
  echo "Python 3.11+ is required."
  exit 1
}
if [ ! -d ".venv" ]; then
  "$PYTHON_BIN" -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address localhost --server.port 8501 --server.headless true
