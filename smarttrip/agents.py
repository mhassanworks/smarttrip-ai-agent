from __future__ import annotations
from dataclasses import dataclass, asdict
import random

@dataclass
class TravelPackage:
    package_id: int
    name: str
    flight: float
    hotel: float
    activities: float
    duration: int
    preference_score: float
    comfort_score: float
    weather_score: float
    utility: float = 0.0

class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.status = "Idle"

class FlightAgent(BaseAgent):
    def propose(self, destination, budget, weather):
        destinations = {"Paris": (620, 780), "Dubai": (550, 720), "Tokyo": (840, 1150),
                        "Bali": (720, 980), "Rome": (600, 760)}
        low, high = destinations.get(destination, (580, 850))
        return {"airfare": round(random.uniform(low, high), 2),
                "carrier": random.choice(["SkyLink", "AeroNova", "CloudJet"]),
                "baggage": "Included"}

class HotelAgent(BaseAgent):
    def propose(self, destination, budget, preference):
        base = {"Paris": 180, "Dubai": 150, "Tokyo": 210, "Bali": 95, "Rome": 160}.get(destination, 150)
        multiplier = 1.25 if "luxury" in preference.lower() else 1.0
        return {"nightly_rate": round(base * multiplier, 2), "stars": 5 if multiplier > 1 else 4,
                "area": "Central district"}

class ActivityAgent(BaseAgent):
    def propose(self, destination, preference, weather):
        catalog = {
            "Paris": ["Louvre", "Seine cruise", "Montmartre"],
            "Dubai": ["Burj Khalifa", "Desert safari", "Marina tour"],
            "Tokyo": ["Senso-ji", "Shibuya", "TeamLab"],
            "Bali": ["Uluwatu", "Ubud", "Nusa Dua"],
            "Rome": ["Colosseum", "Vatican", "Trevi Fountain"],
        }
        activities = catalog.get(destination, ["City tour", "Local market", "Museum"])
        return {"items": activities, "total_cost": 220 if "culture" not in preference.lower() else 260,
                "weather_adjusted": "rain" in weather.lower() or "storm" in weather.lower()}

class BudgetAgent(BaseAgent):
    def validate(self, budget, flight, hotel, activities, days, party_size):
        hotel_total = hotel["nightly_rate"] * max(days - 1, 1)
        total = flight["airfare"] * party_size + hotel_total + activities["total_cost"] * party_size
        return {"estimated_total": round(total, 2), "budget": budget,
                "within_budget": total <= budget, "remaining": round(budget - total, 2)}
