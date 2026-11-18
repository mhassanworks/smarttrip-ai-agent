"""
Assignment 8: Knowledge Representation & Weather API Integration Module

Implements a structured JSON ontological knowledge base for destination profiling,
and integrates real weather forecasts (via Open-Meteo) with high-fidelity mock fallback.
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import httpx

logger = logging.getLogger(__name__)

# Structured Knowledge Representation (Ontology of Popular Destinations)
DESTINATION_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "goa": {
        "city_name": "Goa",
        "state_country": "Goa, India",
        "iata_code": "GOI",
        "coordinates": {"latitude": 15.2993, "longitude": 74.1240},
        "best_season": "November to February",
        "climate_zone": "Tropical Coastal",
        "average_daily_budget_inr": 4500,
        "key_attractions": [
            {"name": "Basilica of Bom Jesus", "type": "Heritage UNESCO", "est_fee_inr": 0, "avg_time_hours": 2.0},
            {"name": "Aguada Fort & Lighthouse", "type": "Historic Fort", "est_fee_inr": 50, "avg_time_hours": 2.5},
            {"name": "Calangute & Baga Beach", "type": "Coastal / Leisure", "est_fee_inr": 0, "avg_time_hours": 3.0},
            {"name": "Dudhsagar Waterfalls", "type": "Nature & Adventure", "est_fee_inr": 500, "avg_time_hours": 5.0},
        ],
        "culinary_highlights": ["Goan Fish Curry", "Pork Vindaloo", "Bebinca", "Feni"],
        "local_transport": ["Scooter Rental (₹400/day)", "Prepaid Taxi", "Local Bus"],
        "travel_tips": "Rent a two-wheeler for scenic coastal travel; respect heritage dress codes in Old Goa churches.",
    },
    "delhi": {
        "city_name": "Delhi",
        "state_country": "Delhi NCR, India",
        "iata_code": "DEL",
        "coordinates": {"latitude": 28.6139, "longitude": 77.2090},
        "best_season": "October to March",
        "climate_zone": "Semi-Arid Continental",
        "average_daily_budget_inr": 3800,
        "key_attractions": [
            {"name": "Qutub Minar", "type": "UNESCO Heritage", "est_fee_inr": 50, "avg_time_hours": 2.0},
            {"name": "Humayun's Tomb", "type": "Mughal Architecture", "est_fee_inr": 50, "avg_time_hours": 2.0},
            {"name": "Red Fort", "type": "Historic Monument", "est_fee_inr": 50, "avg_time_hours": 3.0},
            {"name": "India Gate & Kartavya Path", "type": "National Memorial", "est_fee_inr": 0, "avg_time_hours": 1.5},
        ],
        "culinary_highlights": ["Chole Bhature", "Butter Chicken", "Parathas at Chandni Chowk"],
        "local_transport": ["Delhi Metro (Fast & Air Conditioned)", "Auto Rickshaw", "Uber/Ola"],
        "travel_tips": "Use the Delhi Metro Smart Card to avoid traffic jams; carry a light scarf/jacket in winter.",
    },
    "mumbai": {
        "city_name": "Mumbai",
        "state_country": "Maharashtra, India",
        "iata_code": "BOM",
        "coordinates": {"latitude": 19.0760, "longitude": 72.8777},
        "best_season": "November to February",
        "climate_zone": "Tropical Wet & Dry",
        "average_daily_budget_inr": 5200,
        "key_attractions": [
            {"name": "Gateway of India", "type": "Colonial Monument", "est_fee_inr": 0, "avg_time_hours": 1.5},
            {"name": "Elephanta Caves", "type": "UNESCO Rock-Cut Art", "est_fee_inr": 260, "avg_time_hours": 4.0},
            {"name": "Marine Drive Promenade", "type": "Scenic Waterfront", "est_fee_inr": 0, "avg_time_hours": 2.0},
            {"name": "Chhatrapati Shivaji Terminus", "type": "Victorian Gothic UNESCO", "est_fee_inr": 0, "avg_time_hours": 1.0},
        ],
        "culinary_highlights": ["Vada Pav", "Pav Bhaji", "Bombil Fry", "Irani Chai & Bun Maska"],
        "local_transport": ["Local Train", "Kala-Peela Taxis", "Metro Line 3"],
        "travel_tips": "Sunset at Marine Drive is unmissable; avoid suburban local trains during peak rush hours.",
    },
    "jaipur": {
        "city_name": "Jaipur",
        "state_country": "Rajasthan, India",
        "iata_code": "JAI",
        "coordinates": {"latitude": 26.9124, "longitude": 75.7873},
        "best_season": "October to March",
        "climate_zone": "Hot Semi-Arid",
        "average_daily_budget_inr": 3500,
        "key_attractions": [
            {"name": "Amber Palace & Fort", "type": "Hill Fort UNESCO", "est_fee_inr": 100, "avg_time_hours": 3.5},
            {"name": "Hawa Mahal", "type": "Palace of Winds", "est_fee_inr": 50, "avg_time_hours": 1.5},
            {"name": "City Palace", "type": "Royal Residence", "est_fee_inr": 300, "avg_time_hours": 2.5},
            {"name": "Jantar Mantar", "type": "Astronomical Observatory", "est_fee_inr": 50, "avg_time_hours": 1.5},
        ],
        "culinary_highlights": ["Dal Baati Churma", "Pyaaz Kachori", "Ghewar", "Laal Maas"],
        "local_transport": ["E-Rickshaws", "App Taxis", "Jaipur Metro"],
        "travel_tips": "Buy the composite entry ticket covering 5 major monuments to save time and entry fees.",
    },
    "bengaluru": {
        "city_name": "Bengaluru",
        "state_country": "Karnataka, India",
        "iata_code": "BLR",
        "coordinates": {"latitude": 12.9716, "longitude": 77.5946},
        "best_season": "Year-round (Best: Sept to March)",
        "climate_zone": "Tropical Savanna",
        "average_daily_budget_inr": 4200,
        "key_attractions": [
            {"name": "Lalbagh Botanical Garden", "type": "Botanical Heritage", "est_fee_inr": 30, "avg_time_hours": 2.5},
            {"name": "Bangalore Palace", "type": "Tudor Style Palace", "est_fee_inr": 230, "avg_time_hours": 2.0},
            {"name": "Cubbon Park", "type": "Urban Green Space", "est_fee_inr": 0, "avg_time_hours": 2.0},
            {"name": "National Gallery of Modern Art", "type": "Art Museum", "est_fee_inr": 50, "avg_time_hours": 2.0},
        ],
        "culinary_highlights": ["Filter Coffee", "Benne Dosa", "Mangalore Buns", "Craft Microbreweries"],
        "local_transport": ["Namma Metro", "Auto Rickshaw", "Airport Vayu Vajra Bus"],
        "travel_tips": "Take the Vayu Vajra luxury Volvo bus from the airport; ideal for craft beer & garden walks.",
    },
}


def lookup_destination_knowledge(destination_query: str) -> Dict[str, Any]:
    """Look up structured knowledge profile for a destination."""
    q = destination_query.lower().strip()
    for key, data in DESTINATION_KNOWLEDGE_BASE.items():
        if key in q or data["city_name"].lower() in q:
            return data

    # Default fallback profile for unlisted cities
    return {
        "city_name": destination_query.title(),
        "state_country": f"{destination_query.title()}, Global",
        "iata_code": destination_query[:3].upper(),
        "coordinates": {"latitude": 20.5937, "longitude": 78.9629},
        "best_season": "October to March",
        "climate_zone": "Temperate",
        "average_daily_budget_inr": 4000,
        "key_attractions": [
            {"name": "City Center & Historic Square", "type": "Sightseeing", "est_fee_inr": 0, "avg_time_hours": 2.0},
            {"name": "Regional Heritage Museum", "type": "Cultural", "est_fee_inr": 50, "avg_time_hours": 2.0},
            {"name": "Botanical Waterfront", "type": "Leisure", "est_fee_inr": 20, "avg_time_hours": 1.5},
        ],
        "culinary_highlights": ["Local Regional Specialties", "Street Food Market"],
        "local_transport": ["City Transit", "Rideshare Taxis"],
        "travel_tips": "Check local museum opening hours and carry local currency for transit.",
    }


def fetch_weather_forecast(destination_query: str) -> Dict[str, Any]:
    """
    Fetches real weather from Open-Meteo API using destination coordinates.
    Gracefully falls back to high-fidelity mock weather if offline or network fails.
    """
    profile = lookup_destination_knowledge(destination_query)
    coords = profile["coordinates"]
    lat, lon = coords["latitude"], coords["longitude"]

    data_source = "open_meteo_live"
    weather_info: Dict[str, Any] = {}

    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto"
        resp = httpx.get(url, timeout=3.5)
        if resp.status_code == 200:
            payload = resp.json()
            curr = payload.get("current_weather", {})
            temp_c = curr.get("temperature", 28.0)
            windspeed = curr.get("windspeed", 12.0)
            weathercode = curr.get("weathercode", 0)

            # Map WMO weathercode to descriptive string
            condition = "Clear Sky"
            suitability = 0.95
            if weathercode in [1, 2, 3]:
                condition = "Partly Cloudy"
                suitability = 0.90
            elif weathercode in [45, 48]:
                condition = "Foggy / Mist"
                suitability = 0.75
            elif weathercode in [51, 53, 55, 61, 63, 65, 80, 81]:
                condition = "Light Rain / Showers"
                suitability = 0.65
            elif weathercode >= 70:
                condition = "Heavy Rain / Thunderstorm"
                suitability = 0.40

            weather_info = {
                "temperature_celsius": temp_c,
                "windspeed_kmh": windspeed,
                "condition": condition,
                "suitability_score": suitability,
                "is_outdoor_recommended": suitability >= 0.70,
                "weather_code": weathercode,
            }
        else:
            raise RuntimeError(f"Open-Meteo returned status {resp.status_code}")
    except Exception as exc:
        logger.info("Open-Meteo API unreachable (%s), utilizing high-fidelity mock weather.", exc)
        data_source = "mock_fallback"
        # Deterministic mock weather based on destination
        city_lower = profile["city_name"].lower()
        if "goa" in city_lower:
            weather_info = {
                "temperature_celsius": 29.5,
                "windspeed_kmh": 14.0,
                "condition": "Sunny & Breezy",
                "suitability_score": 0.94,
                "is_outdoor_recommended": True,
                "weather_code": 0,
            }
        elif "delhi" in city_lower:
            weather_info = {
                "temperature_celsius": 23.0,
                "windspeed_kmh": 8.0,
                "condition": "Pleasant & Clear",
                "suitability_score": 0.92,
                "is_outdoor_recommended": True,
                "weather_code": 1,
            }
        elif "mumbai" in city_lower:
            weather_info = {
                "temperature_celsius": 31.0,
                "windspeed_kmh": 16.0,
                "condition": "Humid & Sunny",
                "suitability_score": 0.88,
                "is_outdoor_recommended": True,
                "weather_code": 2,
            }
        else:
            weather_info = {
                "temperature_celsius": 26.0,
                "windspeed_kmh": 10.0,
                "condition": "Partly Cloudy & Mild",
                "suitability_score": 0.90,
                "is_outdoor_recommended": True,
                "weather_code": 1,
            }

    # Generate travel advisory based on weather
    if weather_info["is_outdoor_recommended"]:
        advisory = f"Weather in {profile['city_name']} is {weather_info['condition']} ({weather_info['temperature_celsius']}°C). Ideal for outdoor walking tours and sightseeing."
    else:
        advisory = f"Adverse weather detected in {profile['city_name']}: {weather_info['condition']}. Prioritize indoor museums, galleries, and culinary workshops."

    return {
        "destination": profile["city_name"],
        "data_source": data_source,
        "coordinates": coords,
        "current_weather": weather_info,
        "travel_advisory": advisory,
        "knowledge_profile": profile,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
