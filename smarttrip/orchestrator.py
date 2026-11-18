from __future__ import annotations
from dataclasses import asdict
from .agents import FlightAgent, HotelAgent, ActivityAgent, BudgetAgent
from .rules import ConditionActionEngine, TravelContext
from .utility import rank_packages
from .knowledge import KnowledgeBase
from .bdi import BDIState
from .security import HMACSecurity

class TravelOrchestrator:
    def __init__(self, knowledge):
        self.knowledge = knowledge
        self.rules = ConditionActionEngine()
        self.flight = FlightAgent("Flight Agent")
        self.hotel = HotelAgent("Hotel Agent")
        self.activity = ActivityAgent("Activity Agent")
        self.budget = BudgetAgent("Budget Agent")
        self.bdi = BDIState()
        self.security = HMACSecurity()

    def plan(self, origin, destination, departure, days, budget,
             party_size, preference):
        timeline = []
        destination_info = self.knowledge.get_destination(destination)
        destination_info = destination_info or {"country": "International", "currency": "USD",
                                               "attractions": ["City tour", "Museum", "Local market"]}
        weather = self.knowledge.weather(destination)

        context = TravelContext(budget, party_size, weather["condition"], preference, days)
        rule_result = self.rules.evaluate(context)
        timeline.append({"round": 1, "agent": "Rules Engine", "action": "Rule evaluation",
                         "detail": " | ".join(rule_result["actions"])})

        flight = self.flight.propose(destination, budget, weather["condition"])
        timeline.append({"round": 2, "agent": "Flight Agent", "action": "Initial proposal",
                         "detail": f"{flight['carrier']}: ${flight['airfare']:,.0f} round trip"})
        hotel = self.hotel.propose(destination, budget, preference)
        timeline.append({"round": 2, "agent": "Hotel Agent", "action": "Initial proposal",
                         "detail": f"{hotel['stars']}-star central stay: ${hotel['nightly_rate']:,.0f}/night"})
        activities = self.activity.propose(destination, preference, weather["condition"])
        timeline.append({"round": 2, "agent": "Activity Agent", "action": "Initial proposal",
                         "detail": f"{', '.join(activities['items'])}: ${activities['total_cost']:,.0f}"})

        budget_status = self.budget.validate(budget, flight, hotel, activities, days, party_size)
        timeline.append({"round": 3, "agent": "Budget Agent", "action": "Feasibility check",
                         "detail": f"Estimated ${budget_status['estimated_total']:,.0f} / "
                                   f"${budget:.0f} budget"})

        replanned = False
        if not budget_status["within_budget"]:
            replanned = True
            hotel["nightly_rate"] *= 0.80
            hotel["stars"] = 3
            activities["total_cost"] *= 0.75
            budget_status = self.budget.validate(budget, flight, hotel, activities, days, party_size)
            timeline.append({"round": 4, "agent": "Consensus Group", "action": "Dynamic replan",
                             "detail": "Budget cap exceeded; hotel category and activity cost reduced"})

        packages = rank_packages(destination, days, budget, preference,
                                 weather["condition"], party_size)
        best = packages[0]
        timeline.append({"round": 5, "agent": "Utility Optimizer", "action": "Consensus reached",
                         "detail": f"{best.name} ranked first with utility {best.utility:.3f}"})

        bdi_context = {"destination": destination, "party_size": party_size, "budget": budget}
        self.bdi.update(weather, bdi_context, budget_status)

        return {
            "origin": origin,
            "destination": destination,
            "destination_info": destination_info,
            "departure": departure,
            "days": days,
            "budget": budget,
            "party_size": party_size,
            "preference": preference,
            "weather": weather,
            "rules": rule_result,
            "flight": flight,
            "hotel": hotel,
            "activities": activities,
            "budget_status": budget_status,
            "replanned": replanned,
            "packages": [asdict(p) for p in packages],
            "best_package": asdict(best),
            "timeline": timeline,
            "bdi": {"beliefs": self.bdi.beliefs, "desires": self.bdi.desires,
                    "intentions": self.bdi.intentions},
        }
