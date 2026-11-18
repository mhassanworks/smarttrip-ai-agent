# SmartTrip AI – Autonomous Multi-Agent Travel Planning System

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A complete local Streamlit application that combines rule-based reasoning, BDI replanning, multi-agent negotiation, utility ranking, JSON knowledge, secure TCP communication, HMAC-SHA256, SQLite history and threaded background workers.

## Dashboard Preview

The application provides a responsive dark-navy dashboard with a complete demo and real execution views. Start it locally and open **http://localhost:8501**:

```text
Overview  ->  Travel Planner  ->  Agent Monitoring  ->  Negotiation Timeline
Utility   ->  BDI State       ->  Knowledge Base   ->  Security Logs
```

## Features

- Premium responsive dark dashboard with Plotly visualizations
- Complete one-click autonomous travel planning demonstration
- SQLite-backed execution history and security audit logs
- Real TCP communication between Agent A and Agent B
- HMAC-SHA256 signed JSON messages with tampering rejection
- Thread-safe background workers and latency measurement
- OpenWeather API integration with deterministic mock fallback

## Assignment Mapping

| Assignment | Implementation |
|---|---|
| 1. PEAS and agent analysis | [PEAS profile](docs/PEAS.md) |
| 2. Condition-action rules | `smarttrip/rules.py` |
| 3. Threads, queues and latency | `smarttrip/workers.py` |
| 4. TCP JSON communication | `smarttrip/socket_agent.py` |
| 5. Flight, hotel, activity and budget negotiation | `smarttrip/agents.py`, `smarttrip/orchestrator.py` |
| 6. Mathematical utility ranking | `smarttrip/utility.py` |
| 7. BDI replanning | `smarttrip/bdi.py`, `smarttrip/orchestrator.py` |
| 8. JSON knowledge and weather API | `smarttrip/knowledge.py`, `data/knowledge.json` |
| 9. HMAC-SHA256 security | `smarttrip/security.py` |
| 10. Integrated Streamlit capstone | `app.py` |

## Requirements

- Python 3.11 or newer
- macOS, Linux or Windows
- Internet access is optional; missing weather API credentials trigger mock fallback

## macOS / Linux

```bash
cd /Users/hassan/.copilot/chats/ac261f90-25da-4ab1-8333-c58fc1e8e3a4
chmod +x run.sh
./run.sh
```

## Windows

```bat
cd /d C:\path\to\ac261f90-25da-4ab1-8333-c58fc1e8e3a4
run.bat
```

The launcher creates `.venv`, upgrades pip, installs dependencies and starts:

**http://localhost:8501**

## Manual installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address localhost --server.port 8501
```

For Windows activation: `.venv\Scripts\activate`

## Optional live weather

Set `OPENWEATHER_API_KEY` before launching. If it is missing or the API request fails, the application uses realistic deterministic mock weather.

```bash
export OPENWEATHER_API_KEY="your_key"
```

## Tests

```bash
.venv/bin/python -m pytest -q
```

## Project structure

- `app.py` – premium Streamlit dashboard
- `smarttrip/` – modular agents and system services
- `data/` – knowledge and sample trip data
- `docs/` – PEAS and architecture documentation
- `tests/` – automated unit and workflow tests
- `smarttrip.db` – SQLite execution and security history
