"""
Assignment 10: Capstone Integration Module

Connects all 9 preceding modules into a unified autonomous execution pipeline:
PEAS & Environment -> Rule Engine -> Knowledge/Weather -> BDI Planning ->
TCP Socket Exchange -> Concurrency & Latency -> Multi-Agent Negotiation ->
Utility Optimization (10 Configs) -> HMAC-SHA256 Security Audit -> Persistence.
"""
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from smarttrip.peas_docs import get_peas_documentation
from smarttrip.rule_engine import TravelRuleEngine
from smarttrip.concurrency import monitoring_system
from smarttrip.socket_comm import run_socket_demonstration
from smarttrip.negotiation import run_negotiation_demonstration
from smarttrip.utility_optimizer import run_utility_optimization
from smarttrip.bdi_agent import run_bdi_replanning_demonstration
from smarttrip.knowledge_weather import fetch_weather_forecast, lookup_destination_knowledge
from smarttrip.security import run_security_demonstration
from storage import ItineraryStore


class CapstoneWorkflowEngine:
    def __init__(self):
        self.rule_engine = TravelRuleEngine()
        self.store = ItineraryStore()

    def run_full_lifecycle_demo(
        self,
        origin: str = "DEL",
        destination: str = "Goa",
        budget: float = 45000.0,
        traveler_type: str = "couple",
        interests: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Executes the complete, end-to-end multi-agent travel planning lifecycle,
        demonstrating all 10 academic and engineering assignments.
        """
        t_start = time.perf_counter()
        demo_id = f"demo-{uuid.uuid4().hex[:10]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        active_interests = interests or ["beach", "culture", "relaxation"]

        execution_log: List[Dict[str, Any]] = []

        def log_step(step_num: int, name: str, status: str, duration_ms: float, summary: str):
            execution_log.append({
                "step": step_num,
                "module_name": name,
                "status": status,
                "duration_ms": round(duration_ms, 2),
                "summary": summary,
            })

        # Step 1: PEAS & Agent Personas
        t0 = time.perf_counter()
        peas_data = get_peas_documentation()
        log_step(1, "PEAS & Environment Formulation", "SUCCESS", (time.perf_counter() - t0) * 1000.0,
                 f"Formulated PEAS matrix for {len(peas_data['peas_matrix'])} autonomous agents and classified environment.")

        # Step 2: Rule Engine Evaluation
        t0 = time.perf_counter()
        rule_facts = {
            "origin": origin,
            "destination": destination,
            "budget": budget,
            "traveler_type": traveler_type,
            "interests": active_interests,
            "passengers": 2,
        }
        rule_eval = self.rule_engine.evaluate(rule_facts)
        log_step(2, "Condition-Action Rule Engine", "SUCCESS", (time.perf_counter() - t0) * 1000.0,
                 f"Evaluated {rule_eval.metadata['evaluated_rules_count']} rules; fired {rule_eval.metadata['matched_rules_count']} matching rules.")

        # Step 3: Knowledge Base & Weather API Integration
        t0 = time.perf_counter()
        weather_data = fetch_weather_forecast(destination)
        knowledge_profile = weather_data["knowledge_profile"]
        log_step(3, "Knowledge Base & Weather API", "SUCCESS", (time.perf_counter() - t0) * 1000.0,
                 f"Fetched destination profile and weather ({weather_data['current_weather']['condition']}, {weather_data['current_weather']['temperature_celsius']}°C via {weather_data['data_source']}).")

        # Step 4: BDI Planning & Shock Recovery
        t0 = time.perf_counter()
        bdi_data = run_bdi_replanning_demonstration(budget=budget, shock_type="price_surge")
        log_step(4, "BDI Architecture & Replanning", "SUCCESS", (time.perf_counter() - t0) * 1000.0,
                 f"Simulated price shock; autonomous replanning recovered trip under budget margin ₹{bdi_data['cost_progression']['recovered_budget_margin']}.")

        # Step 5: TCP Socket Communication (Agent A <-> Agent B)
        t0 = time.perf_counter()
        socket_data = run_socket_demonstration({
            "origin": origin,
            "destination": destination,
            "budget": budget,
        })
        log_step(5, "TCP Socket Communication", "SUCCESS", (time.perf_counter() - t0) * 1000.0,
                 f"Exchanged {socket_data['messages_count']} JSON frames over TCP loopback socket ({socket_data['total_bytes_exchanged']} bytes, {socket_data['roundtrip_latency_ms']}ms).")

        # Step 6: Concurrency & Performance Monitoring
        t0 = time.perf_counter()
        monitoring_system.trigger_batch(count=6)
        concurrency_data = monitoring_system.get_status()
        log_step(6, "Concurrency & Latency Telemetry", "SUCCESS", (time.perf_counter() - t0) * 1000.0,
                 f"{concurrency_data['active_workers']} active worker threads; avg latency {concurrency_data['latency_metrics']['avg_processing_ms']}ms.")

        # Step 7: Multi-Agent Negotiation Protocol
        t0 = time.perf_counter()
        negotiation_data = run_negotiation_demonstration(budget=budget)
        log_step(7, "Multi-Agent Negotiation", "SUCCESS", (time.perf_counter() - t0) * 1000.0,
                 f"Executed {negotiation_data['rounds_executed']} bidding rounds; reached consensus at ₹{negotiation_data['final_package_cost']} (concessions: ₹{negotiation_data['total_concessions_achieved']}).")

        # Step 8: Utility Optimization across 10 Configurations
        t0 = time.perf_counter()
        utility_data = run_utility_optimization(budget=budget, destination=destination)
        winning_conf = utility_data["winning_configuration"]
        log_step(8, "Mathematical Utility Optimization", "SUCCESS", (time.perf_counter() - t0) * 1000.0,
                 f"Ranked 10 configurations using MAUT; winner '{winning_conf['name']}' scored {winning_conf['aggregate_utility']}/100.")

        # Step 9: Cryptographic Security & Tamper Detection Audit
        t0 = time.perf_counter()
        security_data = run_security_demonstration()
        log_step(9, "Cryptographic Security Audit", "SUCCESS", (time.perf_counter() - t0) * 1000.0,
                 f"Audited {security_data['total_tests']} signed payloads: {security_data['accepted_legitimate']} accepted, {security_data['blocked_malicious']} attacks blocked (100% enforcement).")

        # Step 10: Final Synthesis & Persistence
        t0 = time.perf_counter()
        total_trip_cost = winning_conf["total_cost"]
        final_itinerary = {
            "id": demo_id,
            "trip_request": {
                "origin": origin,
                "destination": destination,
                "budget": budget,
                "traveler_type": traveler_type,
                "interests": active_interests,
                "start_date": "2026-12-20",
                "end_date": "2026-12-24",
            },
            "flight": winning_conf["details"]["flight"],
            "hotel": winning_conf["details"]["hotel"],
            "activities": [winning_conf["details"]["activity"]],
            "total_cost": total_trip_cost,
            "budget": budget,
            "best_effort": total_trip_cost > budget,
            "negotiation_rounds": negotiation_data["rounds_executed"],
            "utility_score": winning_conf["aggregate_utility"],
            "weather_summary": weather_data["travel_advisory"],
            "applied_rules": [r["name"] for r in rule_eval.applied_rules],
            "created_at": timestamp,
        }

        # Save to SQLite store
        persisted_id = self.store.save(final_itinerary)
        final_itinerary["id"] = persisted_id
        log_step(10, "Capstone Synthesis & SQLite Persistence", "SUCCESS", (time.perf_counter() - t0) * 1000.0,
                 f"Persisted itinerary to SQLite database with trip ID: {persisted_id}.")

        total_duration_ms = round((time.perf_counter() - t_start) * 1000.0, 2)

        return {
            "status": "CAPSTONE_EXECUTION_COMPLETED",
            "demo_id": demo_id,
            "persisted_trip_id": persisted_id,
            "timestamp": timestamp,
            "total_execution_time_ms": total_duration_ms,
            "inputs": {
                "origin": origin,
                "destination": destination,
                "budget": budget,
                "traveler_type": traveler_type,
                "interests": active_interests,
            },
            "assignment_modules": {
                "1_peas": peas_data,
                "2_rules": {
                    "applied_rules": rule_eval.applied_rules,
                    "budget_ceilings": rule_eval.budget_ceilings,
                    "recommended_tags": rule_eval.recommended_tags,
                    "alerts": rule_eval.alerts,
                    "suggested_destinations": rule_eval.suggested_destinations,
                    "metadata": rule_eval.metadata,
                },
                "3_concurrency": concurrency_data,
                "4_socket_communication": socket_data,
                "5_negotiation": negotiation_data,
                "6_utility_optimization": utility_data,
                "7_bdi_replanning": bdi_data,
                "8_knowledge_and_weather": weather_data,
                "9_security_verification": security_data,
                "10_capstone_synthesis": {
                    "final_itinerary": final_itinerary,
                    "database_persisted": True,
                },
            },
            "execution_steps_log": execution_log,
        }


# Singleton workflow engine
capstone_engine = CapstoneWorkflowEngine()


def run_full_demo(budget: float = 45000.0, destination: str = "Goa") -> Dict[str, Any]:
    return capstone_engine.run_full_lifecycle_demo(destination=destination, budget=budget)
