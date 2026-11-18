"""
Assignment 5: Multi-Agent Negotiation Module

Implements a formal Multi-Turn Negotiation Protocol (Contract Net / Alternating Offers)
between Flight, Hotel, Activity, and Budget agents with bidding, concessions, and consensus.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class NegotiationBid:
    agent_id: str
    round_number: int
    category: str
    proposed_cost: float
    specification: str
    tier: str  # "premium", "standard", "economy"
    concession_made: float  # Difference from previous round
    rationale: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class RoundSummary:
    round_number: int
    total_proposed: float
    user_budget: float
    variance: float
    is_within_budget: bool
    bids: List[Dict[str, Any]]
    arbiter_action: str
    consensus_reached: bool


class MultiAgentNegotiator:
    def __init__(self, max_rounds: int = 3):
        self.max_rounds = max_rounds

    def run_negotiation(
        self,
        budget: float,
        origin: str = "DEL",
        destination: str = "GOI",
        force_overage: bool = True,
    ) -> Dict[str, Any]:
        """
        Executes a multi-turn negotiation simulation.
        If force_overage is True or budget is tight, Round 1 starts intentionally
        optimistic (luxury/premium picks that exceed budget) to demonstrate the
        full multi-turn bidding, counter-offering, and consensus convergence.
        """
        user_budget = float(budget)
        history: List[RoundSummary] = []
        negotiation_log: List[Dict[str, Any]] = []

        # Candidate option tiers for each agent
        flight_options = [
            {"tier": "premium", "spec": "Air India Direct Express (Business Class Perks)", "cost": round(user_budget * 0.48, 2)},
            {"tier": "standard", "spec": "IndiGo Non-stop Morning Flight", "cost": round(user_budget * 0.38, 2)},
            {"tier": "economy", "spec": "SpiceJet 1-stop Saver Fare", "cost": round(user_budget * 0.30, 2)},
        ]

        hotel_options = [
            {"tier": "premium", "spec": "Taj Exotica Oceanview Deluxe Suite", "cost": round(user_budget * 0.52, 2)},
            {"tier": "standard", "spec": "Marriott Courtyard Executive Room", "cost": round(user_budget * 0.37, 2)},
            {"tier": "economy", "spec": "Ginger Boutique Standard Room", "cost": round(user_budget * 0.28, 2)},
        ]

        activity_options = [
            {"tier": "premium", "spec": "Private Yacht Charter & Scuba Diving Pass", "cost": round(user_budget * 0.25, 2)},
            {"tier": "standard", "spec": "Guided Heritage Tour & Watersports Combo", "cost": round(user_budget * 0.16, 2)},
            {"tier": "economy", "spec": "Self-Guided Old Goa Walk & Beach Sunset", "cost": round(user_budget * 0.08, 2)},
        ]

        current_flight_idx = 0 if force_overage else 1
        current_hotel_idx = 0 if force_overage else 1
        current_activity_idx = 0 if force_overage else 1

        prev_costs = {"flight": 0.0, "hotel": 0.0, "activity": 0.0}
        consensus = False

        for r in range(1, self.max_rounds + 1):
            curr_f = flight_options[current_flight_idx]
            curr_h = hotel_options[current_hotel_idx]
            curr_a = activity_options[current_activity_idx]

            total_cost = round(curr_f["cost"] + curr_h["cost"] + curr_a["cost"], 2)
            variance = round(total_cost - user_budget, 2)
            within_budget = total_cost <= user_budget

            # Record bids for this round
            f_concession = round(prev_costs["flight"] - curr_f["cost"], 2) if r > 1 else 0.0
            h_concession = round(prev_costs["hotel"] - curr_h["cost"], 2) if r > 1 else 0.0
            a_concession = round(prev_costs["activity"] - curr_a["cost"], 2) if r > 1 else 0.0

            bid_flight = NegotiationBid(
                agent_id="Agent-Flight",
                round_number=r,
                category="flight",
                proposed_cost=curr_f["cost"],
                specification=curr_f["spec"],
                tier=curr_f["tier"],
                concession_made=max(0.0, f_concession),
                rationale=f"Selected {curr_f['tier']} tier route. Conceded ₹{max(0.0, f_concession)} from prior round." if r > 1 else f"Initial bid submitted at {curr_f['tier']} tier.",
            )

            bid_hotel = NegotiationBid(
                agent_id="Agent-Hotel",
                round_number=r,
                category="hotel",
                proposed_cost=curr_h["cost"],
                specification=curr_h["spec"],
                tier=curr_h["tier"],
                concession_made=max(0.0, h_concession),
                rationale=f"Adjusted property to {curr_h['tier']}. Conceded ₹{max(0.0, h_concession)}." if r > 1 else f"Initial lodging bid submitted at {curr_h['tier']} tier.",
            )

            bid_activity = NegotiationBid(
                agent_id="Agent-Activity",
                round_number=r,
                category="activity",
                proposed_cost=curr_a["cost"],
                specification=curr_a["spec"],
                tier=curr_a["tier"],
                concession_made=max(0.0, a_concession),
                rationale=f"Curated {curr_a['tier']} activity itinerary. Conceded ₹{max(0.0, a_concession)}." if r > 1 else f"Initial activities proposed at {curr_a['tier']} tier.",
            )

            round_bids = [vars(bid_flight), vars(bid_hotel), vars(bid_activity)]
            negotiation_log.extend(round_bids)

            prev_costs = {"flight": curr_f["cost"], "hotel": curr_h["cost"], "activity": curr_a["cost"]}

            if within_budget:
                consensus = True
                arbiter_action = f"CONSENSUS REACHED: Package cost ₹{total_cost} is within budget ₹{user_budget} (Surplus: ₹{abs(variance)}). Approved!"
                summary = RoundSummary(
                    round_number=r,
                    total_proposed=total_cost,
                    user_budget=user_budget,
                    variance=variance,
                    is_within_budget=True,
                    bids=round_bids,
                    arbiter_action=arbiter_action,
                    consensus_reached=True,
                )
                history.append(summary)
                break
            else:
                if r == self.max_rounds:
                    arbiter_action = f"MAX ROUNDS EXHAUSTED: Best-effort bundle ratified at ₹{total_cost} (Over budget by ₹{variance}). Ending negotiation."
                    summary = RoundSummary(
                        round_number=r,
                        total_proposed=total_cost,
                        user_budget=user_budget,
                        variance=variance,
                        is_within_budget=False,
                        bids=round_bids,
                        arbiter_action=arbiter_action,
                        consensus_reached=False,
                    )
                    history.append(summary)
                    break
                else:
                    # Arbiter issues targeted concession demand to highest-variance or largest cost category
                    arbiter_action = f"BUDGET OVERRUN: Bundle cost ₹{total_cost} exceeds ₹{user_budget} by ₹{variance}. Demanding concessions from Domain Agents."
                    summary = RoundSummary(
                        round_number=r,
                        total_proposed=total_cost,
                        user_budget=user_budget,
                        variance=variance,
                        is_within_budget=False,
                        bids=round_bids,
                        arbiter_action=arbiter_action,
                        consensus_reached=False,
                    )
                    history.append(summary)

                    # Determine which agents step down tier in the next round
                    if current_hotel_idx < len(hotel_options) - 1:
                        current_hotel_idx += 1
                    if current_flight_idx < len(flight_options) - 1:
                        current_flight_idx += 1
                    if r >= 2 and current_activity_idx < len(activity_options) - 1:
                        current_activity_idx += 1

        final_round = history[-1]
        final_bids = {b["category"]: b for b in final_round.bids}

        total_concessions = (
            (flight_options[0]["cost"] - final_bids["flight"]["proposed_cost"])
            + (hotel_options[0]["cost"] - final_bids["hotel"]["proposed_cost"])
            + (activity_options[0]["cost"] - final_bids["activity"]["proposed_cost"])
        )

        return {
            "status": "CONSENSUS_REACHED" if consensus else "BEST_EFFORT_CONCLUDED",
            "rounds_executed": len(history),
            "max_rounds": self.max_rounds,
            "user_budget": user_budget,
            "final_package_cost": final_round.total_proposed,
            "budget_delta": round(user_budget - final_round.total_proposed, 2),
            "total_concessions_achieved": round(max(0.0, total_concessions), 2),
            "final_selection": {
                "flight": final_bids["flight"],
                "hotel": final_bids["hotel"],
                "activity": final_bids["activity"],
            },
            "rounds_history": [vars(h) for h in history],
            "chronological_log": negotiation_log,
        }


def run_negotiation_demonstration(budget: float = 45000.0) -> Dict[str, Any]:
    """Helper to run negotiation demonstration."""
    negotiator = MultiAgentNegotiator(max_rounds=3)
    return negotiator.run_negotiation(budget=budget, force_overage=True)
