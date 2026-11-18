from __future__ import annotations
import random
from .agents import TravelPackage

def rank_packages(destination: str, days: int, budget: float, preference: str,
                  weather: str, party_size: int, count: int = 10) -> list[TravelPackage]:
    random.seed(sum(ord(c) for c in f"{destination}{days}{preference}") % 10000)
    packages = []
    for i in range(1, count + 1):
        flight = random.uniform(0.19, 0.34) * budget
        hotel = random.uniform(0.24, 0.48) * budget
        activities = random.uniform(0.08, 0.22) * budget
        preference_score = random.uniform(0.55, 0.98)
        comfort_score = random.uniform(0.50, 0.96)
        weather_score = 0.86 if weather in ("Clear skies", "Partly cloudy", "Hot and sunny") else 0.68
        if preference.lower() in ("luxury", "relaxation") and i % 3 == 0:
            comfort_score += 0.04
        utility = (
            0.28 * (1 - min(flight + hotel + activities, budget) / budget)
            + 0.27 * preference_score
            + 0.25 * comfort_score
            + 0.20 * weather_score
        )
        packages.append(TravelPackage(
            i, f"{destination} Escape {i}", round(flight, 2), round(hotel, 2),
            round(activities, 2), days, round(preference_score, 3),
            round(min(comfort_score, 1), 3), round(weather_score, 3),
            round(utility, 4),
        ))
    return sorted(packages, key=lambda p: p.utility, reverse=True)
