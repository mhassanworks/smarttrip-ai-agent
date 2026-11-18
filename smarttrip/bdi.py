from __future__ import annotations

class BDIState:
    def __init__(self):
        self.beliefs = {}
        self.desires = []
        self.intentions = []

    def update(self, weather: dict, context: dict, budget_status: dict):
        self.beliefs = {
            "weather": weather,
            "destination": context["destination"],
            "party_size": context["party_size"],
            "budget_available": context["budget"],
            "budget_within_limit": budget_status["within_budget"],
        }
        self.desires = [
            "Build a complete itinerary",
            "Keep total cost within budget",
            "Match traveler preferences",
        ]
        if not budget_status["within_budget"]:
            self.intentions = [
                "Replan: reduce hotel category",
                "Replan: shift to lower-cost flight",
                "Replan: replace premium activities",
            ]
        else:
            self.intentions = [
                "Finalize preferred flight",
                "Reserve central hotel",
                "Sequence weather-adjusted activities",
            ]
