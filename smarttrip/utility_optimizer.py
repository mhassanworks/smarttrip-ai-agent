"""
Assignment 6: Utility Optimization Module

Implements Multi-Attribute Utility Theory (MAUT) to evaluate, score,
and rank 10 distinct travel configurations, selecting the globally optimal configuration.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class UtilityWeights:
    budget_weight: float = 0.35
    rating_weight: float = 0.25
    convenience_weight: float = 0.20
    weather_weight: float = 0.20

    def validate(self) -> bool:
        total = self.budget_weight + self.rating_weight + self.convenience_weight + self.weather_weight
        return abs(total - 1.0) < 0.001


@dataclass
class TravelConfiguration:
    config_id: str
    name: str
    archetype: str
    flight_name: str
    flight_price: float
    stops: int
    transit_duration_hours: float
    airline_rating: float  # Out of 5.0
    hotel_name: str
    hotel_price: float
    hotel_stars: float  # Out of 5.0
    hotel_rating: float  # Out of 5.0
    activity_package: str
    activity_price: float
    weather_suitability: float  # 0.0 to 1.0
    tags: List[str] = field(default_factory=list)

    @property
    def total_cost(self) -> float:
        return round(self.flight_price + self.hotel_price + self.activity_price, 2)


@dataclass
class ScoredConfiguration:
    rank: int
    config_id: str
    name: str
    archetype: str
    total_cost: float
    cost_variance: float
    sub_utilities: Dict[str, float]  # Scaled 0 to 100
    aggregate_utility: float  # Scaled 0 to 100
    details: Dict[str, Any]
    formula_breakdown: str


class UtilityOptimizer:
    def __init__(self, weights: Optional[UtilityWeights] = None):
        self.weights = weights or UtilityWeights()

    def generate_ten_configurations(self, budget: float, destination: str = "Goa") -> List[TravelConfiguration]:
        """Generates exactly 10 diverse, realistic travel configurations."""
        b = float(budget)
        return [
            TravelConfiguration(
                config_id="CONF-01",
                name="Budget Backpacker Saver",
                archetype="Cost Minimizer",
                flight_name="SpiceJet SG-192 (1 Stop)",
                flight_price=round(b * 0.24, 2),
                stops=1,
                transit_duration_hours=5.5,
                airline_rating=3.6,
                hotel_name="Zostel Beach Hostel Private Pod",
                hotel_price=round(b * 0.22, 2),
                hotel_stars=3.0,
                hotel_rating=4.3,
                activity_package="Self-guided Beach Walk & Fort Aguada",
                activity_price=round(b * 0.08, 2),
                weather_suitability=0.88,
                tags=["budget", "hostel", "social"],
            ),
            TravelConfiguration(
                config_id="CONF-02",
                name="Balanced Smart Explorer",
                archetype="Balanced Value",
                flight_name="IndiGo 6E-502 (Non-stop)",
                flight_price=round(b * 0.34, 2),
                stops=0,
                transit_duration_hours=2.5,
                airline_rating=4.4,
                hotel_name="Lemon Tree Resort & Spa",
                hotel_price=round(b * 0.36, 2),
                hotel_stars=4.0,
                hotel_rating=4.5,
                activity_package="Heritage Church Walk & Sunset Catamaran",
                activity_price=round(b * 0.16, 2),
                weather_suitability=0.92,
                tags=["balanced", "comfortable", "scenic"],
            ),
            TravelConfiguration(
                config_id="CONF-03",
                name="Direct Flight Comfort Priority",
                archetype="Transit Optimized",
                flight_name="Air India AI-880 Premium Economy",
                flight_price=round(b * 0.42, 2),
                stops=0,
                transit_duration_hours=2.2,
                airline_rating=4.2,
                hotel_name="Hyatt Place Candolim",
                hotel_price=round(b * 0.34, 2),
                hotel_stars=4.0,
                hotel_rating=4.4,
                activity_package="Old Goa Basilica & Spice Plantation",
                activity_price=round(b * 0.14, 2),
                weather_suitability=0.90,
                tags=["fast-transit", "direct-flight", "relaxed"],
            ),
            TravelConfiguration(
                config_id="CONF-04",
                name="Heritage & Cultural Boutique",
                archetype="Culture Focused",
                flight_name="Vistara UK-841 (Direct)",
                flight_price=round(b * 0.36, 2),
                stops=0,
                transit_duration_hours=2.4,
                airline_rating=4.6,
                hotel_name="Fort Tiracol Heritage Boutique Hotel",
                hotel_price=round(b * 0.42, 2),
                hotel_stars=4.5,
                hotel_rating=4.8,
                activity_package="Private Historian Tour & Museum Passes",
                activity_price=round(b * 0.18, 2),
                weather_suitability=0.85,
                tags=["boutique", "historic", "architecture"],
            ),
            TravelConfiguration(
                config_id="CONF-05",
                name="Coastal Luxury Executive",
                archetype="Premium Indulgence",
                flight_name="Vistara UK-992 Business Class",
                flight_price=round(b * 0.48, 2),
                stops=0,
                transit_duration_hours=2.2,
                airline_rating=4.8,
                hotel_name="Taj Exotica Resort & Spa",
                hotel_price=round(b * 0.52, 2),
                hotel_stars=5.0,
                hotel_rating=4.9,
                activity_package="Private Luxury Yacht & Scuba Diving",
                activity_price=round(b * 0.22, 2),
                weather_suitability=0.95,
                tags=["luxury", "5-star", "vip"],
            ),
            TravelConfiguration(
                config_id="CONF-06",
                name="Action & Watersports Adventure",
                archetype="Experiential Adventure",
                flight_name="Akasa Air QP-1301 (Direct)",
                flight_price=round(b * 0.30, 2),
                stops=0,
                transit_duration_hours=2.6,
                airline_rating=4.1,
                hotel_name="Resort Rio Arpora",
                hotel_price=round(b * 0.32, 2),
                hotel_stars=4.0,
                hotel_rating=4.2,
                activity_package="Parasailing, Jet Ski & Bungee Jump Pass",
                activity_price=round(b * 0.28, 2),
                weather_suitability=0.94,
                tags=["adventure", "watersports", "adrenaline"],
            ),
            TravelConfiguration(
                config_id="CONF-07",
                name="Scenic Nature & Leisure Retreat",
                archetype="Wellness & Relaxation",
                flight_name="IndiGo 6E-212 (Morning Saver)",
                flight_price=round(b * 0.32, 2),
                stops=0,
                transit_duration_hours=2.5,
                airline_rating=4.3,
                hotel_name="Alila Diwa Eco-Resort & Spa",
                hotel_price=round(b * 0.40, 2),
                hotel_stars=4.5,
                hotel_rating=4.7,
                activity_package="Ayurvedic Wellness Session & Bird Sanctuary Walk",
                activity_price=round(b * 0.15, 2),
                weather_suitability=0.91,
                tags=["eco-friendly", "wellness", "spa"],
            ),
            TravelConfiguration(
                config_id="CONF-08",
                name="Off-Peak Value Maximizer",
                archetype="Smart Deal",
                flight_name="Air India Express IX-711 (Evening)",
                flight_price=round(b * 0.27, 2),
                stops=1,
                transit_duration_hours=4.2,
                airline_rating=3.9,
                hotel_name="BloomSuites Calangute",
                hotel_price=round(b * 0.30, 2),
                hotel_stars=3.5,
                hotel_rating=4.3,
                activity_package="Anjuna Flea Market & Beach Sunset Drinks",
                activity_price=round(b * 0.11, 2),
                weather_suitability=0.86,
                tags=["off-peak", "value", "nightlife"],
            ),
            TravelConfiguration(
                config_id="CONF-09",
                name="Family Suite Comfort Bundle",
                archetype="Family Priority",
                flight_name="IndiGo 6E-789 (Midday Direct)",
                flight_price=round(b * 0.36, 2),
                stops=0,
                transit_duration_hours=2.4,
                airline_rating=4.4,
                hotel_name="Novotel Goa Resort & Pool Suites",
                hotel_price=round(b * 0.38, 2),
                hotel_stars=4.0,
                hotel_rating=4.4,
                activity_package="Dolphin Spotting Cruise & Waterpark Day Pass",
                activity_price=round(b * 0.17, 2),
                weather_suitability=0.89,
                tags=["family", "kid-friendly", "pool-access"],
            ),
            TravelConfiguration(
                config_id="CONF-10",
                name="Culinary & Nightlife Epicurean",
                archetype="Gourmet Experience",
                flight_name="Vistara UK-855 (Direct)",
                flight_price=round(b * 0.35, 2),
                stops=0,
                transit_duration_hours=2.4,
                airline_rating=4.5,
                hotel_name="W Goa Vagator Beachfront",
                hotel_price=round(b * 0.46, 2),
                hotel_stars=5.0,
                hotel_rating=4.8,
                activity_package="Chef-Led Goan Food Trail & Sunset Club Reservation",
                activity_price=round(b * 0.20, 2),
                weather_suitability=0.93,
                tags=["culinary", "nightlife", "luxury"],
            ),
        ]

    def evaluate_configuration(self, config: TravelConfiguration, user_budget: float) -> ScoredConfiguration:
        cost = config.total_cost
        b = float(user_budget)
        w = self.weights

        # 1. Budget Sub-Utility U_b: Linear penalty for exceeding budget, reward for staying within
        if cost <= b:
            # Under budget: normalized score 75 to 100 based on savings
            savings_pct = (b - cost) / b
            u_budget = min(100.0, 75.0 + (savings_pct * 100.0 * 0.75))
        else:
            # Over budget: penalty decays rapidly
            overage_pct = (cost - b) / b
            u_budget = max(0.0, 75.0 - (overage_pct * 180.0))

        # 2. Rating Sub-Utility U_r: Blended score of airline (30%) and hotel (70%)
        # Both ratings are on 0 to 5 scale
        blended_stars = (config.airline_rating * 0.3) + (config.hotel_rating * 0.7)
        u_rating = round((blended_stars / 5.0) * 100.0, 2)

        # 3. Convenience Sub-Utility U_c: Penalizes layover stops and transit duration
        # Baseline 100 minus stop penalty (20 per stop) minus transit penalty (4 per hour above 2h)
        stop_penalty = config.stops * 20.0
        transit_penalty = max(0.0, (config.transit_duration_hours - 2.0) * 4.0)
        u_convenience = max(10.0, min(100.0, 100.0 - stop_penalty - transit_penalty))

        # 4. Weather Sub-Utility U_w: Direct mapping of 0.0 - 1.0 suitability
        u_weather = round(config.weather_suitability * 100.0, 2)

        # Weighted aggregate utility
        u_aggregate = (
            (w.budget_weight * u_budget)
            + (w.rating_weight * u_rating)
            + (w.convenience_weight * u_convenience)
            + (w.weather_weight * u_weather)
        )
        u_aggregate = round(u_aggregate, 2)

        formula_breakdown = (
            f"U = ({w.budget_weight} × {round(u_budget, 1)}) + "
            f"({w.rating_weight} × {round(u_rating, 1)}) + "
            f"({w.convenience_weight} × {round(u_convenience, 1)}) + "
            f"({w.weather_weight} × {round(u_weather, 1)}) = {u_aggregate}"
        )

        return ScoredConfiguration(
            rank=0,  # Filled after sorting
            config_id=config.config_id,
            name=config.name,
            archetype=config.archetype,
            total_cost=cost,
            cost_variance=round(cost - b, 2),
            sub_utilities={
                "budget_efficiency": round(u_budget, 2),
                "quality_rating": round(u_rating, 2),
                "transit_convenience": round(u_convenience, 2),
                "weather_suitability": round(u_weather, 2),
            },
            aggregate_utility=u_aggregate,
            details={
                "flight": {
                    "name": config.flight_name,
                    "price": config.flight_price,
                    "stops": config.stops,
                    "duration_hours": config.transit_duration_hours,
                    "rating": config.airline_rating,
                },
                "hotel": {
                    "name": config.hotel_name,
                    "price": config.hotel_price,
                    "stars": config.hotel_stars,
                    "rating": config.hotel_rating,
                },
                "activity": {
                    "package": config.activity_package,
                    "price": config.activity_price,
                },
                "weather_score": config.weather_suitability,
                "tags": config.tags,
            },
            formula_breakdown=formula_breakdown,
        )

    def optimize_and_rank(self, budget: float, destination: str = "Goa") -> Dict[str, Any]:
        """Generates 10 configurations, evaluates mathematical utility, and ranks them."""
        configs = self.generate_ten_configurations(budget=budget, destination=destination)
        scored = [self.evaluate_configuration(c, budget) for c in configs]

        # Sort descending by aggregate utility
        scored.sort(key=lambda s: s.aggregate_utility, reverse=True)

        for i, item in enumerate(scored):
            item.rank = i + 1

        winner = scored[0]

        return {
            "status": "OPTIMIZATION_COMPLETE",
            "mathematical_model": "Multi-Attribute Utility Theory (MAUT)",
            "formula": "U(c) = w_b·U_b(c) + w_r·U_r(c) + w_c·U_c(c) + w_w·U_w(c)",
            "weights": vars(self.weights),
            "user_budget": float(budget),
            "total_options_evaluated": len(scored),
            "winning_configuration": vars(winner),
            "ranked_configurations": [vars(s) for s in scored],
        }


def run_utility_optimization(budget: float = 45000.0, destination: str = "Goa") -> Dict[str, Any]:
    """Helper to run the utility optimization."""
    optimizer = UtilityOptimizer()
    return optimizer.optimize_and_rank(budget=budget, destination=destination)
