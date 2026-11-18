from __future__ import annotations
import json
from pathlib import Path
import requests
from .config import WEATHER_API_KEY, WEATHER_URL

class KnowledgeBase:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.path = self.data_path / "knowledge.json"
        if not self.path.exists():
            self._write_default()
        self.data = self.load()

    def _write_default(self):
        default = {
            "destinations": {
                "Paris": {"country": "France", "currency": "EUR", "attractions": ["Louvre", "Eiffel Tower", "Montmartre"]},
                "Dubai": {"country": "UAE", "currency": "AED", "attractions": ["Burj Khalifa", "Desert Safari", "Dubai Museum"]},
                "Tokyo": {"country": "Japan", "currency": "JPY", "attractions": ["Shibuya", "Senso-ji", "Tsukiji"]},
                "Bali": {"country": "Indonesia", "currency": "IDR", "attractions": ["Uluwatu", "Ubud", "Nusa Dua"]},
                "Rome": {"country": "Italy", "currency": "EUR", "attractions": ["Colosseum", "Vatican", "Trevi Fountain"]}
            },
            "rules": ["Protect budget first", "Weather-adjust activities", "Preserve preference fit"]
        }
        self.path.write_text(json.dumps(default, indent=2), encoding="utf-8")

    def load(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_destination(self, name):
        return self.data["destinations"].get(name)

    def weather(self, destination: str) -> dict:
        if WEATHER_API_KEY:
            try:
                response = requests.get(
                    WEATHER_URL,
                    params={"q": destination, "appid": WEATHER_API_KEY, "units": "metric"},
                    timeout=5,
                )
                response.raise_for_status()
                payload = response.json()
                condition = payload["weather"][0]["description"].title()
                return {
                    "source": "OpenWeather API",
                    "condition": condition,
                    "temperature": round(payload["main"]["temp"], 1),
                    "humidity": payload["main"]["humidity"],
                }
            except (requests.RequestException, KeyError, ValueError):
                pass
        seed = sum(ord(c) for c in destination.lower()) % 4
        options = [
            ("Clear skies", 26, 48),
            ("Light rain", 21, 72),
            ("Partly cloudy", 23, 58),
            ("Hot and sunny", 31, 44),
        ]
        condition, temperature, humidity = options[seed]
        return {"source": "Mock weather fallback", "condition": condition,
                "temperature": temperature, "humidity": humidity}
