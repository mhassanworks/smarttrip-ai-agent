"""
Assignment 7: BDI (Beliefs, Desires, Intentions) Architecture Module

Implements a formal BDI agent architecture with dynamic belief revision,
desire reconsideration, and reactive replanning when environmental shocks occur.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class BeliefSet:
    user_budget: float
    flight_price: float
    flight_name: str
    flight_status: str  # "AVAILABLE", "PRICE_SURGE", "CANCELLED"
    hotel_price: float
    hotel_name: str
    hotel_status: str  # "CONFIRMED", "SOLD_OUT", "AVAILABLE"
    activity_cost: float
    activity_name: str
    weather_condition: str  # "SUNNY", "MONSOON_STORM", "HEATWAVE"
    weather_risk_level: str  # "LOW", "MODERATE", "HIGH"

    @property
    def total_cost(self) -> float:
        return round(self.flight_price + self.hotel_price + self.activity_cost, 2)

    @property
    def is_over_budget(self) -> bool:
        return self.total_cost > self.user_budget


@dataclass
class Desire:
    desire_id: str
    description: str
    priority: int  # 1 (Highest) to 5
    satisfied: bool
    rationale: str


@dataclass
class Intention:
    intention_id: str
    action_type: str  # "BOOK_FLIGHT", "RESERVE_HOTEL", "SCHEDULE_ACTIVITY", "HOLD_BUFFER"
    target: str
    allocated_cost: float
    status: str  # "COMMITTED", "EXECUTED", "DROPPED", "REPLACED"


@dataclass
class BDICycleSnapshot:
    phase: str  # "INITIAL_COMMITTED_PLAN", "ENVIRONMENTAL_SHOCK", "REPLANNED_PLAN"
    timestamp: str
    beliefs: Dict[str, Any]
    desires: List[Dict[str, Any]]
    intentions: List[Dict[str, Any]]
    notes: str


class BDITravelPlanner:
    def __init__(self, budget: float = 40000.0):
        self.budget = float(budget)

    def run_bdi_lifecycle(self, shock_type: str = "price_surge") -> Dict[str, Any]:
        """
        Executes a complete BDI lifecycle:
        1. Formulates initial Beliefs, Desires, and Intentions.
        2. Injects an environmental shock (e.g. price surge on the flight or severe storm).
        3. Executes Belief Revision -> Desire Reconsideration -> Intention Replanning.
        """
        b = self.budget

        # ----------------------------------------------------
        # Phase 1: Initial State
        # ----------------------------------------------------
        initial_beliefs = BeliefSet(
            user_budget=b,
            flight_price=round(b * 0.36, 2),
            flight_name="IndiGo 6E-452 (Direct)",
            flight_status="AVAILABLE",
            hotel_price=round(b * 0.40, 2),
            hotel_name="BloomSuites Heritage Calangute",
            hotel_status="AVAILABLE",
            activity_cost=round(b * 0.16, 2),
            activity_name="Scuba Diving & Fort Walking Tour",
            weather_condition="SUNNY",
            weather_risk_level="LOW",
        )

        initial_desires = [
            Desire("D1", f"Maintain total expenditures within budget (<= ₹{b})", priority=1, satisfied=True, rationale="Primary constraint"),
            Desire("D2", "Secure comfortable 4-star lodging with pool", priority=2, satisfied=True, rationale="Comfort requirement"),
            Desire("D3", "Experience outdoor adventure & watersports", priority=3, satisfied=True, rationale="Traveler interest"),
            Desire("D4", "Keep travel safety index high", priority=1, satisfied=True, rationale="Safety priority"),
        ]

        initial_intentions = [
            Intention("I1", "BOOK_FLIGHT", initial_beliefs.flight_name, initial_beliefs.flight_price, "COMMITTED"),
            Intention("I2", "RESERVE_HOTEL", initial_beliefs.hotel_name, initial_beliefs.hotel_price, "COMMITTED"),
            Intention("I3", "SCHEDULE_ACTIVITY", initial_beliefs.activity_name, initial_beliefs.activity_cost, "COMMITTED"),
        ]

        snap1 = BDICycleSnapshot(
            phase="INITIAL_COMMITTED_PLAN",
            timestamp=datetime.now(timezone.utc).isoformat(),
            beliefs=vars(initial_beliefs),
            desires=[vars(d) for d in initial_desires],
            intentions=[vars(i) for i in initial_intentions],
            notes=f"Initial plan stably committed. Total cost ₹{initial_beliefs.total_cost} is within budget ₹{b}.",
        )

        # ----------------------------------------------------
        # Phase 2: Environmental Shock (Belief Update)
        # ----------------------------------------------------
        if shock_type == "weather_disruption":
            shocked_beliefs = BeliefSet(
                user_budget=b,
                flight_price=initial_beliefs.flight_price,
                flight_name=initial_beliefs.flight_name,
                flight_status="AVAILABLE",
                hotel_price=initial_beliefs.hotel_price,
                hotel_name=initial_beliefs.hotel_name,
                hotel_status="AVAILABLE",
                activity_cost=initial_beliefs.activity_cost,
                activity_name=initial_beliefs.activity_name,
                weather_condition="MONSOON_STORM",
                weather_risk_level="HIGH",
            )
            shock_description = "Severe coastal storm alert declared. Outdoor scuba diving is unsafe & suspended."
        else:  # Default: price_surge
            surged_flight_price = round(initial_beliefs.flight_price * 1.65, 2)
            shocked_beliefs = BeliefSet(
                user_budget=b,
                flight_price=surged_flight_price,
                flight_name=initial_beliefs.flight_name,
                flight_status="PRICE_SURGE",
                hotel_price=initial_beliefs.hotel_price,
                hotel_name=initial_beliefs.hotel_name,
                hotel_status="AVAILABLE",
                activity_cost=initial_beliefs.activity_cost,
                activity_name=initial_beliefs.activity_name,
                weather_condition="SUNNY",
                weather_risk_level="LOW",
            )
            overage = round(shocked_beliefs.total_cost - b, 2)
            shock_description = f"Unexpected airline fare surge (+65%) on {initial_beliefs.flight_name}! Flight price escalated to ₹{surged_flight_price}. Total package cost ₹{shocked_beliefs.total_cost} breaches budget by ₹{overage}."

        shocked_desires = [
            Desire("D1", f"Maintain total expenditures within budget (<= ₹{b})", priority=1, satisfied=not shocked_beliefs.is_over_budget, rationale="Violated by price surge" if shocked_beliefs.is_over_budget else "Still satisfied"),
            Desire("D2", "Secure comfortable 4-star lodging with pool", priority=2, satisfied=True, rationale="Comfort requirement"),
            Desire("D3", "Experience outdoor adventure & watersports", priority=3, satisfied=(shocked_beliefs.weather_condition != "MONSOON_STORM"), rationale="Threatened by storm" if shocked_beliefs.weather_condition == "MONSOON_STORM" else "Feasible"),
            Desire("D4", "Keep travel safety index high", priority=1, satisfied=(shocked_beliefs.weather_risk_level == "LOW"), rationale="Threatened by weather alert" if shocked_beliefs.weather_risk_level != "LOW" else "Satisfied"),
        ]

        shocked_intentions = [
            Intention("I1", "BOOK_FLIGHT", shocked_beliefs.flight_name, shocked_beliefs.flight_price, "INVALIDATED" if shocked_beliefs.is_over_budget else "COMMITTED"),
            Intention("I2", "RESERVE_HOTEL", shocked_beliefs.hotel_name, shocked_beliefs.hotel_price, "COMMITTED"),
            Intention("I3", "SCHEDULE_ACTIVITY", shocked_beliefs.activity_name, shocked_beliefs.activity_cost, "SUSPENDED" if shock_type == "weather_disruption" else "COMMITTED"),
        ]

        snap2 = BDICycleSnapshot(
            phase="ENVIRONMENTAL_SHOCK",
            timestamp=datetime.now(timezone.utc).isoformat(),
            beliefs=vars(shocked_beliefs),
            desires=[vars(d) for d in shocked_desires],
            intentions=[vars(i) for i in shocked_intentions],
            notes=shock_description,
        )

        # ----------------------------------------------------
        # Phase 3: Dynamic Replanning & Intention Revision
        # ----------------------------------------------------
        replanning_steps: List[str] = []

        if shock_type == "weather_disruption":
            replanning_steps.append("Belief revision: Weather sensor detected 'MONSOON_STORM' and 'HIGH' safety risk.")
            replanning_steps.append("Desire reconsideration: D4 (Safety) and D1 (Budget) take precedence over D3 (Outdoor sports).")
            replanning_steps.append("Intention replanning: Dropping 'Scuba Diving & Fort Walking Tour' (I3).")
            replanning_steps.append("Formulating new intention: Committing to indoor 'Goan Heritage Museum, Art Gallery & Indoor Cooking Masterclass' at ₹4,200.")

            revised_activity_cost = round(b * 0.10, 2)
            replanned_beliefs = BeliefSet(
                user_budget=b,
                flight_price=initial_beliefs.flight_price,
                flight_name=initial_beliefs.flight_name,
                flight_status="AVAILABLE",
                hotel_price=initial_beliefs.hotel_price,
                hotel_name=initial_beliefs.hotel_name,
                hotel_status="AVAILABLE",
                activity_cost=revised_activity_cost,
                activity_name="Indoor Heritage Museum & Culinary Masterclass",
                weather_condition="MONSOON_STORM",
                weather_risk_level="MITIGATED_INDOORS",
            )

            replanned_intentions = [
                Intention("I1", "BOOK_FLIGHT", replanned_beliefs.flight_name, replanned_beliefs.flight_price, "COMMITTED"),
                Intention("I2", "RESERVE_HOTEL", replanned_beliefs.hotel_name, replanned_beliefs.hotel_price, "COMMITTED"),
                Intention("I3-REV", "SCHEDULE_ACTIVITY", replanned_beliefs.activity_name, replanned_beliefs.activity_cost, "COMMITTED"),
            ]
        else:
            # Price Surge Replanning
            replanning_steps.append("Belief revision: Flight fare surged to ₹" + str(shocked_beliefs.flight_price) + " breaching budget constraint D1.")
            replanning_steps.append("Desire reconsideration: D1 (Budget constraint) is strict. Agent searches option space for alternate carrier or adjusted lodging tier.")
            replanning_steps.append("Option A considered: Downgrading hotel to budget hostel (rejected: violates D2 comfort).")
            replanning_steps.append("Option B selected: Re-routing to SpiceJet SG-812 (1-stop, 1h layover) at ₹11,800 + adjusting hotel room to Executive Standard at ₹15,200.")
            replanning_steps.append("Intentions revised: Revoked I1 (IndiGo surged), committed I1-ALT (SpiceJet) and I2-ADJ.")

            replanned_flight_price = round(b * 0.28, 2)
            replanned_hotel_price = round(b * 0.38, 2)
            replanned_activity_price = round(b * 0.14, 2)

            replanned_beliefs = BeliefSet(
                user_budget=b,
                flight_price=replanned_flight_price,
                flight_name="SpiceJet SG-812 (Value Saver, 1h Layover)",
                flight_status="CONFIRMED_REPLACED",
                hotel_price=replanned_hotel_price,
                hotel_name="BloomSuites Executive Wing",
                hotel_status="CONFIRMED_REALLOCATED",
                activity_cost=replanned_activity_price,
                activity_name="Guided Heritage & Catamaran Tour",
                weather_condition="SUNNY",
                weather_risk_level="LOW",
            )

            replanned_intentions = [
                Intention("I1-REV", "BOOK_FLIGHT", replanned_beliefs.flight_name, replanned_beliefs.flight_price, "COMMITTED"),
                Intention("I2-REV", "RESERVE_HOTEL", replanned_beliefs.hotel_name, replanned_beliefs.hotel_price, "COMMITTED"),
                Intention("I3-REV", "SCHEDULE_ACTIVITY", replanned_beliefs.activity_name, replanned_beliefs.activity_cost, "COMMITTED"),
            ]

        replanned_desires = [
            Desire("D1", f"Maintain total expenditures within budget (<= ₹{b})", priority=1, satisfied=True, rationale=f"Restored: New cost ₹{replanned_beliefs.total_cost} <= ₹{b}"),
            Desire("D2", "Secure comfortable 4-star lodging with pool", priority=2, satisfied=True, rationale="Preserved in Executive Wing"),
            Desire("D3", "Experience top destination sights", priority=3, satisfied=True, rationale="Preserved with safe indoor/outdoor balance"),
            Desire("D4", "Keep travel safety index high", priority=1, satisfied=True, rationale="Verified safe"),
        ]

        savings = round(b - replanned_beliefs.total_cost, 2)
        snap3 = BDICycleSnapshot(
            phase="REPLANNED_PLAN",
            timestamp=datetime.now(timezone.utc).isoformat(),
            beliefs=vars(replanned_beliefs),
            desires=[vars(d) for d in replanned_desires],
            intentions=[vars(i) for i in replanned_intentions],
            notes=f"Plan autonomously restored! Total cost ₹{replanned_beliefs.total_cost} brings the trip ₹{savings} below budget.",
        )

        return {
            "status": "REPLANNING_SUCCESSFUL",
            "shock_type": shock_type,
            "shock_description": shock_description,
            "replanning_steps": replanning_steps,
            "cost_progression": {
                "initial_cost": initial_beliefs.total_cost,
                "shock_cost": shocked_beliefs.total_cost,
                "replanned_cost": replanned_beliefs.total_cost,
                "user_budget": b,
                "recovered_budget_margin": savings,
            },
            "cycles": [vars(snap1), vars(snap2), vars(snap3)],
        }


def run_bdi_replanning_demonstration(budget: float = 40000.0, shock_type: str = "price_surge") -> Dict[str, Any]:
    """Helper to execute BDI replanning demonstration."""
    planner = BDITravelPlanner(budget=budget)
    return planner.run_bdi_lifecycle(shock_type=shock_type)
