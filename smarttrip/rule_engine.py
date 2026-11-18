"""
Assignment 2: Rule Engine Module

Production Condition-Action Rule Engine implementing forward-chaining
heuristics for travel preferences, budget thresholds, and destination selection.
"""
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
from datetime import date


@dataclass
class Rule:
    rule_id: str
    name: str
    category: str  # "preference", "budget", "destination", "seasonal"
    priority: int  # Higher priority rules execute first
    description: str
    condition: Callable[[Dict[str, Any]], bool]
    action: Callable[[Dict[str, Any], Dict[str, Any]], None]


@dataclass
class RuleEvaluationResult:
    applied_rules: List[Dict[str, Any]] = field(default_factory=list)
    budget_ceilings: Dict[str, float] = field(default_factory=dict)
    recommended_tags: List[str] = field(default_factory=list)
    alerts: List[str] = field(default_factory=list)
    suggested_destinations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TravelRuleEngine:
    def __init__(self):
        self.rules: List[Rule] = []
        self._register_default_rules()

    def register_rule(self, rule: Rule) -> None:
        self.rules.append(rule)
        # Keep rules sorted by priority descending
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def _register_default_rules(self) -> None:
        # Rule 1: Family Trip Configuration
        def is_family(facts: Dict[str, Any]) -> bool:
            traveler_type = str(facts.get("traveler_type", "")).lower()
            passengers = facts.get("passengers", 1)
            return traveler_type == "family" or passengers >= 3

        def apply_family(facts: Dict[str, Any], output: Dict[str, Any]) -> None:
            output["recommended_tags"].extend(["kid-friendly", "spacious", "direct-flights-preferred"])
            output["alerts"].append("Family traveling: Enforcing kid-friendly activity filters and direct flight preference.")
            # Shift budget slightly towards hotel for larger rooms / suites
            ceilings = output["budget_ceilings"]
            total = facts.get("budget", 50000.0)
            ceilings["flight"] = round(total * 0.38, 2)
            ceilings["hotel"] = round(total * 0.44, 2)
            ceilings["activity"] = round(total * 0.18, 2)

        self.register_rule(Rule(
            rule_id="RULE-PREF-01",
            name="Family Travel Policy",
            category="preference",
            priority=90,
            description="Adjusts category allocations and tags for family groups (prioritizes lodging comfort).",
            condition=is_family,
            action=apply_family,
        ))

        # Rule 2: Solo Backpacker Preference
        def is_solo(facts: Dict[str, Any]) -> bool:
            traveler_type = str(facts.get("traveler_type", "")).lower()
            passengers = facts.get("passengers", 1)
            return traveler_type == "solo" or passengers == 1

        def apply_solo(facts: Dict[str, Any], output: Dict[str, Any]) -> None:
            output["recommended_tags"].extend(["social-hostels", "walking-tours", "adventure", "flexible-transit"])
            # Solo travelers spend more on activities/exploration, less on luxury lodging
            ceilings = output["budget_ceilings"]
            total = facts.get("budget", 30000.0)
            ceilings["flight"] = round(total * 0.40, 2)
            ceilings["hotel"] = round(total * 0.32, 2)
            ceilings["activity"] = round(total * 0.28, 2)

        self.register_rule(Rule(
            rule_id="RULE-PREF-02",
            name="Solo Backpacker Policy",
            category="preference",
            priority=85,
            description="Increases activity budget allocation for solo travelers seeking experiential tours.",
            condition=is_solo,
            action=apply_solo,
        ))

        # Rule 3: Couple / Honeymoon Preference
        def is_couple(facts: Dict[str, Any]) -> bool:
            traveler_type = str(facts.get("traveler_type", "")).lower()
            return traveler_type in ["couple", "honeymoon", "romantic"]

        def apply_couple(facts: Dict[str, Any], output: Dict[str, Any]) -> None:
            output["recommended_tags"].extend(["romantic-dining", "boutique-resorts", "sunset-cruises", "scenic"])
            ceilings = output["budget_ceilings"]
            total = facts.get("budget", 50000.0)
            ceilings["flight"] = round(total * 0.35, 2)
            ceilings["hotel"] = round(total * 0.45, 2)
            ceilings["activity"] = round(total * 0.20, 2)

        self.register_rule(Rule(
            rule_id="RULE-PREF-03",
            name="Couple Romance Policy",
            category="preference",
            priority=85,
            description="Prioritizes boutique accommodations and scenic/dining experiences.",
            condition=is_couple,
            action=apply_couple,
        ))

        # Rule 4: Ultra-Budget Threshold (< 25,000 INR)
        def is_ultra_budget(facts: Dict[str, Any]) -> bool:
            budget = float(facts.get("budget", 40000.0))
            return budget < 25000.0

        def apply_ultra_budget(facts: Dict[str, Any], output: Dict[str, Any]) -> None:
            output["alerts"].append("Tight budget detected (< ₹25,000): Enforcing strict economy tier, free municipal sights, and budget carriers.")
            output["recommended_tags"].extend(["budget-saver", "public-transit", "free-entry-monuments"])

        self.register_rule(Rule(
            rule_id="RULE-BUDGET-01",
            name="Ultra-Budget Constraint",
            category="budget",
            priority=95,
            description="Triggers strict cost conservation and low-cost transport/lodging filters.",
            condition=is_ultra_budget,
            action=apply_ultra_budget,
        ))

        # Rule 5: Luxury Tier Threshold (> 90,000 INR)
        def is_luxury(facts: Dict[str, Any]) -> bool:
            budget = float(facts.get("budget", 40000.0))
            return budget >= 90000.0

        def apply_luxury(facts: Dict[str, Any], output: Dict[str, Any]) -> None:
            output["alerts"].append("Luxury tier budget (>= ₹90,000): Unlocking 5-star properties, private airport transfers, and premium experiences.")
            output["recommended_tags"].extend(["5-star-luxury", "private-guides", "business-class", "fine-dining"])

        self.register_rule(Rule(
            rule_id="RULE-BUDGET-02",
            name="Luxury Tier Experience",
            category="budget",
            priority=92,
            description="Unlocks premium filters, high-end activities, and upscale lodging.",
            condition=is_luxury,
            action=apply_luxury,
        ))

        # Rule 6: Beach & Relaxation Destination Matcher
        def is_beach_seeker(facts: Dict[str, Any]) -> bool:
            interests = [str(i).lower() for i in facts.get("interests", [])]
            return any(k in interests for k in ["beach", "sea", "coastal", "relaxation", "surfing"])

        def apply_beach(facts: Dict[str, Any], output: Dict[str, Any]) -> None:
            output["suggested_destinations"].extend(["Goa", "Kerala", "Andaman", "Phuket", "Gokarna"])
            output["recommended_tags"].extend(["water-sports", "beachfront", "coastal-dining"])

        self.register_rule(Rule(
            rule_id="RULE-DEST-01",
            name="Coastal & Beach Matching",
            category="destination",
            priority=75,
            description="Suggests top beach destinations when travelers express interest in coastal relaxation.",
            condition=is_beach_seeker,
            action=apply_beach,
        ))

        # Rule 7: Mountain & Trekking Destination Matcher
        def is_mountain_seeker(facts: Dict[str, Any]) -> bool:
            interests = [str(i).lower() for i in facts.get("interests", [])]
            return any(k in interests for k in ["mountains", "trekking", "hiking", "hills", "snow", "adventure"])

        def apply_mountain(facts: Dict[str, Any], output: Dict[str, Any]) -> None:
            output["suggested_destinations"].extend(["Manali", "Leh Ladakh", "Shimla", "Darjeeling", "Rishikesh"])
            output["recommended_tags"].extend(["trekking-routes", "valley-views", "altitude-clothing"])

        self.register_rule(Rule(
            rule_id="RULE-DEST-02",
            name="Mountain & Alpine Matching",
            category="destination",
            priority=75,
            description="Recommends alpine and hill retreat destinations for adventure and nature enthusiasts.",
            condition=is_mountain_seeker,
            action=apply_mountain,
        ))

        # Rule 8: Heritage & Culture Destination Matcher
        def is_culture_seeker(facts: Dict[str, Any]) -> bool:
            interests = [str(i).lower() for i in facts.get("interests", [])]
            return any(k in interests for k in ["culture", "history", "heritage", "monuments", "architecture", "temples"])

        def apply_culture(facts: Dict[str, Any], output: Dict[str, Any]) -> None:
            output["suggested_destinations"].extend(["Jaipur", "Delhi", "Agra", "Varanasi", "Udaipur", "Hampi"])
            output["recommended_tags"].extend(["monument-passes", "guided-walks", "unesco-sites", "museums"])

        self.register_rule(Rule(
            rule_id="RULE-DEST-03",
            name="Heritage & Cultural Exploration",
            category="destination",
            priority=75,
            description="Matches cultural and historical travelers with UNESCO heritage cities.",
            condition=is_culture_seeker,
            action=apply_culture,
        ))

        # Rule 9: Seasonal Monsoon Warning (July - August in Hill Stations)
        def is_monsoon_hill_risk(facts: Dict[str, Any]) -> bool:
            dest = str(facts.get("destination", "")).lower()
            start_date = facts.get("start_date")
            month = 0
            if isinstance(start_date, (date, str)):
                try:
                    s_str = str(start_date)
                    month = int(s_str.split("-")[1])
                except Exception:
                    pass
            is_hill = any(h in dest for h in ["manali", "shimla", "dharamsala", "kedarnath", "rishikesh"])
            return is_hill and month in [7, 8]

        def apply_monsoon_risk(facts: Dict[str, Any], output: Dict[str, Any]) -> None:
            output["alerts"].append("Monsoon advisory: Traveling to northern hill regions in July/August carries landslide and road-closure risk. Advise flexible bookings.")
            output["recommended_tags"].append("travel-insurance-recommended")

        self.register_rule(Rule(
            rule_id="RULE-SEASON-01",
            name="Monsoon Mountain Advisory",
            category="seasonal",
            priority=88,
            description="Flags weather and terrain safety concerns during monsoon season in mountain zones.",
            condition=is_monsoon_hill_risk,
            action=apply_monsoon_risk,
        ))

    def evaluate(self, facts: Dict[str, Any]) -> RuleEvaluationResult:
        """Evaluates all registered rules against the provided facts."""
        total_budget = float(facts.get("budget", 40000.0))
        # Initial baseline split: 40% flight, 40% hotel, 20% activity
        default_ceilings = {
            "flight": round(total_budget * 0.40, 2),
            "hotel": round(total_budget * 0.40, 2),
            "activity": round(total_budget * 0.20, 2),
        }

        context = {
            "budget_ceilings": default_ceilings,
            "recommended_tags": [],
            "alerts": [],
            "suggested_destinations": [],
        }

        applied = []
        for rule in self.rules:
            try:
                if rule.condition(facts):
                    rule.action(facts, context)
                    applied.append({
                        "rule_id": rule.rule_id,
                        "name": rule.name,
                        "category": rule.category,
                        "priority": rule.priority,
                        "description": rule.description,
                    })
            except Exception as exc:
                context["alerts"].append(f"Rule {rule.rule_id} evaluation failed: {exc}")

        # Deduplicate tags and destinations
        unique_tags = list(dict.fromkeys(context["recommended_tags"]))
        unique_destinations = list(dict.fromkeys(context["suggested_destinations"]))

        return RuleEvaluationResult(
            applied_rules=applied,
            budget_ceilings=context["budget_ceilings"],
            recommended_tags=unique_tags,
            alerts=context["alerts"],
            suggested_destinations=unique_destinations,
            metadata={
                "evaluated_rules_count": len(self.rules),
                "matched_rules_count": len(applied),
                "total_budget": total_budget,
            },
        )
