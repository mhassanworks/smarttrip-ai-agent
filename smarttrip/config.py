from __future__ import annotations
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "smarttrip.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
SOCKET_HOST = "127.0.0.1"
SOCKET_PORT = 8765
