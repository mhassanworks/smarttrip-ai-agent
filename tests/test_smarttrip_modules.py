"""
Automated Test Suite for SmartTrip AI Modules (Assignments 1 through 10).

Validates:
- Assignment 1: PEAS matrices and environment classification structures
- Assignment 2: Rule engine condition-action heuristics, budgets, and tags
- Assignment 3: Multi-threaded concurrency, queue handling, locks, and latency tracking
- Assignment 4: TCP socket client-server framed JSON exchange
- Assignment 5: Multi-agent negotiation bidding, concessions, and consensus
- Assignment 6: Multi-Attribute Utility Optimization (10 ranked configurations)
- Assignment 7: BDI dynamic replanning upon environmental price surge / storm
- Assignment 8: Destination knowledge base and weather API integration
- Assignment 9: HMAC-SHA256 signature verification, tampering detection, and replay blocking
- Assignment 10: Capstone end-to-end integration and SQLite persistence
"""
import time
import pytest
from fastapi.testclient import TestClient

from api.main import app
from smarttrip.peas_docs import get_peas_documentation, PEAS_MATRIX, ENVIRONMENT_CLASSIFICATIONS
from smarttrip.rule_engine import TravelRuleEngine
from smarttrip.concurrency import BackgroundMonitoringSystem, monitoring_system
from smarttrip.socket_comm import SocketExchangeRunner, run_socket_demonstration
from smarttrip.negotiation import MultiAgentNegotiator, run_negotiation_demonstration
from smarttrip.utility_optimizer import UtilityOptimizer, run_utility_optimization
from smarttrip.bdi_agent import BDITravelPlanner, run_bdi_replanning_demonstration
from smarttrip.knowledge_weather import fetch_weather_forecast, lookup_destination_knowledge, DESTINATION_KNOWLEDGE_BASE
from smarttrip.security import AgentSecurityManager, SignedMessage, run_security_demonstration
from smarttrip.capstone import capstone_engine, run_full_demo


client = TestClient(app)


# ============================================================================
# ASSIGNMENT 1: PEAS & Environment Tests
# ============================================================================
def test_assignment_1_peas_matrix():
    data = get_peas_documentation()
    assert "peas_matrix" in data
    assert len(data["peas_matrix"]) >= 8

    agent_names = [a["agent"] for a in data["peas_matrix"]]
    assert "Flight Agent" in agent_names
    assert "Hotel Agent" in agent_names
    assert "Pricing & Budget Agent" in agent_names
    assert "BDI Planner Agent" in agent_names
    assert "Security & Verification Agent" in agent_names

    # Check environment classifications
    assert len(data["environment_classifications"]) >= 5
    dims = [e["dimension"] for e in data["environment_classifications"]]
    assert "Observability" in dims
    assert "Determinism" in dims
    assert "Dynamism" in dims

    # Check Agent vs OOP
    assert len(data["agent_vs_oop"]) >= 5


def test_api_peas_endpoint():
    res = client.get("/api/peas")
    assert res.status_code == 200
    json_data = res.json()
    assert "peas_matrix" in json_data


# ============================================================================
# ASSIGNMENT 2: Condition-Action Rule Engine Tests
# ============================================================================
def test_assignment_2_family_rule():
    engine = TravelRuleEngine()
    facts = {
        "traveler_type": "family",
        "passengers": 4,
        "budget": 60000.0,
        "interests": ["culture", "kid-friendly"],
    }
    result = engine.evaluate(facts)
    assert any(r["rule_id"] == "RULE-PREF-01" for r in result.applied_rules)
    assert "kid-friendly" in result.recommended_tags
    # Family allocation gives more to hotel
    assert result.budget_ceilings["hotel"] > result.budget_ceilings["activity"]


def test_assignment_2_budget_rules():
    engine = TravelRuleEngine()
    # Ultra-budget test
    low_res = engine.evaluate({"budget": 20000.0, "traveler_type": "solo"})
    assert any(r["rule_id"] == "RULE-BUDGET-01" for r in low_res.applied_rules)

    # Luxury test
    lux_res = engine.evaluate({"budget": 100000.0, "traveler_type": "couple"})
    assert any(r["rule_id"] == "RULE-BUDGET-02" for r in lux_res.applied_rules)
    assert any("5-star" in tag for tag in lux_res.recommended_tags)


def test_api_rules_endpoint():
    payload = {
        "origin": "DEL",
        "destination": "Goa",
        "budget": 45000.0,
        "traveler_type": "solo",
        "interests": ["beach", "adventure"],
        "passengers": 1,
    }
    res = client.post("/api/rules/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "applied_rules" in data
    assert len(data["applied_rules"]) >= 2
    assert "budget_ceilings" in data


# ============================================================================
# ASSIGNMENT 3: Concurrency & Performance Monitoring Tests
# ============================================================================
def test_assignment_3_concurrency_workers():
    system = BackgroundMonitoringSystem(num_workers=2, max_history=20)
    try:
        t_ids = system.trigger_batch(count=4)
        assert len(t_ids) == 4
        time.sleep(0.08)  # Let worker threads process tasks
        status = system.get_status()
        assert status["active_workers"] == 2
        assert status["total_tasks_processed"] >= 1
        assert "latency_metrics" in status
        assert status["latency_metrics"]["avg_processing_ms"] >= 0.0
    finally:
        system.stop()


def test_api_concurrency_endpoints():
    res1 = client.get("/api/concurrency/status")
    assert res1.status_code == 200
    assert "worker_threads" in res1.json()

    res2 = client.post("/api/concurrency/trigger?count=3")
    assert res2.status_code == 200
    data = res2.json()
    assert data["status"] == "BATCH_ENQUEUED"
    assert len(data["task_ids"]) == 3


# ============================================================================
# ASSIGNMENT 4: TCP Socket Communication Tests
# ============================================================================
def test_assignment_4_socket_communication():
    result = run_socket_demonstration({
        "origin": "DEL",
        "destination": "GOI",
        "budget": 35000.0,
    })
    assert result["status"] == "SUCCESS"
    assert result["messages_count"] >= 4
    assert result["total_bytes_exchanged"] > 100
    assert result["roundtrip_latency_ms"] >= 0.0
    roles = [m["role"] for m in result["transcript"]]
    assert any("Agent A" in r for r in roles)
    assert any("Agent B" in r for r in roles)


def test_api_socket_endpoint():
    res = client.post("/api/socket/run-exchange", json={"origin": "BOM", "destination": "GOI", "budget": 40000.0})
    assert res.status_code == 200
    assert res.json()["status"] == "SUCCESS"


# ============================================================================
# ASSIGNMENT 5: Multi-Agent Negotiation Tests
# ============================================================================
def test_assignment_5_negotiation_consensus():
    negotiator = MultiAgentNegotiator(max_rounds=3)
    res = negotiator.run_negotiation(budget=50000.0, force_overage=True)
    assert res["status"] in ["CONSENSUS_REACHED", "BEST_EFFORT_CONCLUDED"]
    assert res["rounds_executed"] >= 1
    assert "final_selection" in res
    assert "flight" in res["final_selection"]
    assert "hotel" in res["final_selection"]
    assert "activity" in res["final_selection"]
    assert len(res["chronological_log"]) >= 3


def test_api_negotiation_endpoint():
    res = client.post("/api/negotiation/run", json={"budget": 42000.0, "max_rounds": 3, "force_overage": True})
    assert res.status_code == 200
    data = res.json()
    assert data["user_budget"] == 42000.0
    assert len(data["rounds_history"]) >= 1


# ============================================================================
# ASSIGNMENT 6: Utility Optimization Tests (10 Options)
# ============================================================================
def test_assignment_6_utility_ranking_ten_options():
    res = run_utility_optimization(budget=40000.0, destination="Goa")
    assert res["status"] == "OPTIMIZATION_COMPLETE"
    assert res["total_options_evaluated"] == 10
    configs = res["ranked_configurations"]
    assert len(configs) == 10

    # Ensure ranked monotonically descending
    for i in range(len(configs) - 1):
        assert configs[i]["rank"] == i + 1
        assert configs[i]["aggregate_utility"] >= configs[i + 1]["aggregate_utility"]

    winner = res["winning_configuration"]
    assert winner["rank"] == 1
    assert "formula_breakdown" in winner
    assert "sub_utilities" in winner
    assert winner["sub_utilities"]["budget_efficiency"] >= 0.0


def test_api_utility_endpoint():
    res = client.post("/api/utility/optimize", json={"budget": 48000.0, "destination": "Goa"})
    assert res.status_code == 200
    data = res.json()
    assert len(data["ranked_configurations"]) == 10


# ============================================================================
# ASSIGNMENT 7: BDI Architecture & Replanning Tests
# ============================================================================
def test_assignment_7_bdi_price_surge_replanning():
    res = run_bdi_replanning_demonstration(budget=40000.0, shock_type="price_surge")
    assert res["status"] == "REPLANNING_SUCCESSFUL"
    assert len(res["cycles"]) == 3
    # Check that initial cycle is within budget
    assert res["cycles"][0]["phase"] == "INITIAL_COMMITTED_PLAN"
    # Check shock cycle was over budget
    assert res["cycles"][1]["phase"] == "ENVIRONMENTAL_SHOCK"
    assert res["cycles"][1]["beliefs"]["flight_status"] == "PRICE_SURGE"
    # Check replanned cycle recovered
    assert res["cycles"][2]["phase"] == "REPLANNED_PLAN"
    assert res["cost_progression"]["recovered_budget_margin"] >= 0.0


def test_assignment_7_bdi_storm_replanning():
    res = run_bdi_replanning_demonstration(budget=40000.0, shock_type="weather_disruption")
    assert res["status"] == "REPLANNING_SUCCESSFUL"
    assert res["cycles"][1]["beliefs"]["weather_condition"] == "MONSOON_STORM"
    assert "MITIGATED_INDOORS" in res["cycles"][2]["beliefs"]["weather_risk_level"]


def test_api_bdi_endpoint():
    res = client.post("/api/bdi/replan", json={"budget": 45000.0, "shock_type": "price_surge"})
    assert res.status_code == 200
    assert res.json()["status"] == "REPLANNING_SUCCESSFUL"


# ============================================================================
# ASSIGNMENT 8: Knowledge Base & Weather API Tests
# ============================================================================
def test_assignment_8_destination_knowledge():
    profile = lookup_destination_knowledge("Goa")
    assert profile["city_name"] == "Goa"
    assert len(profile["key_attractions"]) >= 3
    assert "coordinates" in profile


def test_assignment_8_weather_fallback():
    weather = fetch_weather_forecast("Goa")
    assert "current_weather" in weather
    assert "temperature_celsius" in weather["current_weather"]
    assert "condition" in weather["current_weather"]
    assert "travel_advisory" in weather
    assert weather["data_source"] in ["open_meteo_live", "mock_fallback"]


def test_api_knowledge_and_weather_endpoints():
    res1 = client.get("/api/knowledge/destination/delhi")
    assert res1.status_code == 200
    assert res1.json()["city_name"] == "Delhi"

    res2 = client.get("/api/weather/mumbai")
    assert res2.status_code == 200
    assert "current_weather" in res2.json()


# ============================================================================
# ASSIGNMENT 9: Cryptographic Security & HMAC-SHA256 Tests
# ============================================================================
def test_assignment_9_hmac_signing_and_tampering():
    sec = AgentSecurityManager()
    payload = {"flight": "AI-101", "cost": 15000.0}
    msg = sec.sign_message("Agent-Flight", "Agent-Coordinator", payload)

    # 1. Verification of legitimate message
    audit1 = sec.verify_message(msg)
    assert audit1.is_valid is True
    assert audit1.status_code == "ACCEPTED"

    # 2. Tampering detection
    tampered_msg = SignedMessage(
        sender_id=msg.sender_id,
        recipient_id=msg.recipient_id,
        timestamp=msg.timestamp,
        nonce="new-nonce-1234",
        payload={"flight": "AI-101", "cost": 100.0},  # Altered!
        signature=msg.signature,
    )
    audit2 = sec.verify_message(tampered_msg)
    assert audit2.is_valid is False
    assert audit2.status_code == "TAMPERING_DETECTED"

    # 3. Unauthorized sender rejection
    unauth_msg = sec.sign_message("Attacker-Bot", "Agent-Coordinator", {"steal": True})
    audit3 = sec.verify_message(unauth_msg)
    assert audit3.is_valid is False
    assert audit3.status_code == "UNAUTHORIZED_SENDER"


def test_assignment_9_security_audit_demo():
    res = run_security_demonstration()
    assert res["total_tests"] == 5
    assert res["accepted_legitimate"] == 1
    assert res["blocked_malicious"] == 4
    assert res["security_enforcement_rate_pct"] == 100.0


def test_api_security_endpoints():
    res = client.get("/api/security/audit")
    assert res.status_code == 200
    assert res.json()["security_enforcement_rate_pct"] == 100.0


# ============================================================================
# ASSIGNMENT 10: Capstone Integration & Complete Lifecycle Tests
# ============================================================================
def test_assignment_10_capstone_demo_execution():
    result = capstone_engine.run_full_lifecycle_demo(
        origin="DEL",
        destination="Goa",
        budget=45000.0,
        traveler_type="couple",
    )
    assert result["status"] == "CAPSTONE_EXECUTION_COMPLETED"
    assert "persisted_trip_id" in result
    assert result["total_execution_time_ms"] > 0

    # Ensure all 10 modules produced outputs
    modules = result["assignment_modules"]
    assert "1_peas" in modules
    assert "2_rules" in modules
    assert "3_concurrency" in modules
    assert "4_socket_communication" in modules
    assert "5_negotiation" in modules
    assert "6_utility_optimization" in modules
    assert "7_bdi_replanning" in modules
    assert "8_knowledge_and_weather" in modules
    assert "9_security_verification" in modules
    assert "10_capstone_synthesis" in modules

    # Check execution step logs
    assert len(result["execution_steps_log"]) == 10


def test_api_demo_run_and_history():
    res = client.post("/api/demo/run", json={"destination": "Goa", "budget": 40000.0})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "CAPSTONE_EXECUTION_COMPLETED"

    hist_res = client.get("/api/demo/history")
    assert hist_res.status_code == 200
    assert len(hist_res.json()) >= 1
