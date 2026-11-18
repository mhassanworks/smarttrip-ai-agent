from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class TravelContext:
    budget: float
    party_size: int
    weather: str
    preference: str
    days: int

class ConditionActionEngine:
    def evaluate(self, context: TravelContext) -> dict:
        actions = []
        per_person = context.budget / max(context.party_size, 1)
        if per_person < 900:
            actions.append("Budget-first: prioritize economy flights and 3-star hotels")
        elif per_person > 2200:
            actions.append("Premium: allow flexible fares and 4-5 star hotels")
        else:
            actions.append("Balanced: optimize cost and comfort")
        weather = context.weather.lower()
        if any(word in weather for word in ("rain", "storm", "snow")):
            actions.append("Indoor activities: museums, galleries and covered attractions")
        elif "hot" in weather or "clear" in weather:
            actions.append("Outdoor activities: parks, tours and waterfront experiences")
        else:
            actions.append("Mixed-weather: keep one indoor and one outdoor option")
        preference = context.preference.lower()
        if "adventure" in preference:
            actions.append("Adventure weighting: trails, diving and activity passes")
        elif "culture" in preference:
            actions.append("Culture weighting: heritage, museums and local cuisine")
        elif "relax" in preference:
            actions.append("Relaxation weighting: spas, beaches and low-intensity itineraries")
        else:
            actions.append("Balanced weighting: blend culture, food and sightseeing")
        return {"actions": actions, "per_person_budget": round(per_person, 2)}
