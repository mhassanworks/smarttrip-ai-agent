"""
FastAPI layer exposing the travel planner graph and SmartTrip AI multi-agent modules over HTTP.

POST /plan-trip streams progress via Server-Sent Events as the graph
executes — one event per node completion (flight_agent, hotel_agent,
activity_agent, pricing_agent, reallocate, synthesize).

Also provides REST endpoints for all 10 academic multi-agent assignments:
- /api/peas (PEAS & Environment specifications)
- /api/rules/evaluate (Condition-Action Rule Engine)
- /api/concurrency/status & /api/concurrency/trigger (Background workers & latency)
- /api/socket/run-exchange (TCP Socket client-server communication)
- /api/negotiation/run (Multi-turn proposal, bidding, and consensus)
- /api/utility/optimize (MAUT utility optimization of 10 configurations)
- /api/bdi/replan (BDI belief revision & dynamic replanning)
- /api/knowledge/destination & /api/weather (Knowledge base & live weather)
- /api/security/audit & /api/security/verify (HMAC-SHA256 signature verification)
- /api/demo/run & /api/demo/history (One-click complete lifecycle capstone integration)
"""
import json
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, ValidationError

from config import settings
from schemas.messages import TripRequest
from graph.state import build_initial_state
from graph.build import build_travel_planner_graph
from storage import ItineraryStore

# SmartTrip Multi-Agent Modules
from smarttrip.peas_docs import get_peas_documentation
from smarttrip.rule_engine import TravelRuleEngine
from smarttrip.concurrency import monitoring_system
from smarttrip.socket_comm import run_socket_demonstration
from smarttrip.negotiation import run_negotiation_demonstration, MultiAgentNegotiator
from smarttrip.utility_optimizer import run_utility_optimization, UtilityOptimizer
from smarttrip.bdi_agent import run_bdi_replanning_demonstration, BDITravelPlanner
from smarttrip.knowledge_weather import fetch_weather_forecast, lookup_destination_knowledge, DESTINATION_KNOWLEDGE_BASE
from smarttrip.security import run_security_demonstration, AgentSecurityManager, SignedMessage
from smarttrip.capstone import run_full_demo, capstone_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.cors_is_wildcard:
        logger.warning("CORS is set to '*' (allow all origins). Set CORS_ALLOWED_ORIGINS in .env before deploying.")
    if not settings.redis_url:
        logger.warning("Using in-memory cache (not shared across workers). Set REDIS_URL for multi-worker deployments.")
    # Ensure monitoring system is active
    monitoring_system.start()
    yield
    monitoring_system.stop()


app = FastAPI(
    title="SmartTrip AI — Autonomous Multi-Agent Travel Planning & Negotiation System",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_graph = build_travel_planner_graph()
_store = ItineraryStore()
_rule_engine = TravelRuleEngine()
_security_manager = AgentSecurityManager()


def _sse_event(event: str, data: dict) -> str:
    """Formats a single SSE frame."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


async def _stream_trip_plan(request: TripRequest, max_negotiation_rounds: int) -> AsyncGenerator[str, None]:
    initial_state = build_initial_state(request, max_negotiation_rounds=max_negotiation_rounds)

    try:
        for step in _graph.stream(initial_state, stream_mode="updates"):
            for node_name, update in step.items():
                node_messages = update.get("message_log", [])
                data_source = node_messages[-1].payload.get("data_source") if node_messages else None

                yield _sse_event("node_complete", {
                    "node": node_name,
                    "status": update.get("status"),
                    "is_over_budget": update.get("is_over_budget"),
                    "negotiation_round": update.get("negotiation_round"),
                    "data_source": data_source,
                })

                if node_name == "synthesize" and update.get("final_itinerary"):
                    final_itinerary = update["final_itinerary"]
                    trip_id = _store.save(final_itinerary)
                    final_itinerary["id"] = trip_id
                    yield _sse_event("itinerary_ready", final_itinerary)

    except Exception as exc:
        yield _sse_event("error", {"message": str(exc)})
        return

    yield _sse_event("done", {})


@app.post("/plan-trip")
@app.post("/api/plan-trip")
async def plan_trip(request: dict):
    try:
        trip_request = TripRequest(**{k: v for k, v in request.items() if k != "max_negotiation_rounds"})
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors())

    max_rounds = request.get("max_negotiation_rounds", 3)

    return StreamingResponse(
        _stream_trip_plan(trip_request, max_rounds),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/trips")
@app.get("/api/trips")
async def list_trips():
    return _store.list_all()


@app.get("/trips/{trip_id}")
@app.get("/api/trips/{trip_id}")
async def get_trip(trip_id: str):
    trip = _store.get(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@app.delete("/trips/{trip_id}")
@app.delete("/api/trips/{trip_id}")
async def delete_trip(trip_id: str):
    if not _store.delete(trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"status": "deleted"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/health")
async def api_health():
    return {
        "status": "healthy",
        "service": "SmartTrip AI",
        "version": "2.0.0",
        "monitoring_workers_active": monitoring_system.get_status()["active_workers"],
    }


@app.get("/api/status")
async def system_status():
    """Comprehensive system status across all agents and services."""
    return {
        "system": "SmartTrip AI Multi-Agent Platform",
        "version": "2.0.0",
        "status": "OPERATIONAL",
        "registered_agents": [
            "Flight Agent",
            "Hotel Agent",
            "Activity Agent",
            "Pricing Arbiter",
            "BDI Dynamic Planner",
            "TCP Socket Coordinator",
            "HMAC Security Verifier",
            "Concurrent Telemetry Worker",
        ],
        "concurrency": monitoring_system.get_status(),
        "database": "SQLite (Thread-safe ItineraryStore)",
        "weather_service": "Open-Meteo REST API (with mock fallback)",
    }


# ============================================================================
# ASSIGNMENT 1: PEAS & Environment
# ============================================================================
@app.get("/api/peas")
async def get_peas():
    """Returns PEAS specification, environment classifications, and Agent vs OOP analysis."""
    return get_peas_documentation()


# ============================================================================
# ASSIGNMENT 2: Condition-Action Rule Engine
# ============================================================================
class RuleEvaluationRequest(BaseModel):
    origin: str = "DEL"
    destination: str = "Goa"
    budget: float = 40000.0
    traveler_type: str = "couple"
    interests: list[str] = Field(default_factory=lambda: ["beach", "culture"])
    passengers: int = 2


@app.post("/api/rules/evaluate")
async def evaluate_rules(request: RuleEvaluationRequest):
    """Evaluates condition-action rules against travel facts."""
    facts = request.model_dump()
    result = _rule_engine.evaluate(facts)
    return {
        "applied_rules": result.applied_rules,
        "budget_ceilings": result.budget_ceilings,
        "recommended_tags": result.recommended_tags,
        "alerts": result.alerts,
        "suggested_destinations": result.suggested_destinations,
        "metadata": result.metadata,
    }


# ============================================================================
# ASSIGNMENT 3: Concurrency & Performance Monitoring
# ============================================================================
@app.get("/api/concurrency/status")
async def get_concurrency_status():
    """Returns live worker thread metrics, queue depth, and latency statistics."""
    return monitoring_system.get_status()


@app.post("/api/concurrency/trigger")
async def trigger_concurrency_batch(count: int = Query(default=5, ge=1, le=50)):
    """Triggers background monitoring tasks to record live processing latencies."""
    task_ids = monitoring_system.trigger_batch(count=count)
    return {
        "status": "BATCH_ENQUEUED",
        "task_count": len(task_ids),
        "task_ids": task_ids,
        "telemetry": monitoring_system.get_status(),
    }


# ============================================================================
# ASSIGNMENT 4: TCP Socket Communication
# ============================================================================
class SocketDemoRequest(BaseModel):
    origin: str = "DEL"
    destination: str = "GOI"
    departure_date: str = "2026-12-20"
    budget: float = 45000.0


@app.post("/api/socket/run-exchange")
async def run_socket_exchange(request: Optional[SocketDemoRequest] = None):
    """Runs a complete low-level TCP client-server exchange with JSON serialization."""
    req_dict = request.model_dump() if request else None
    return run_socket_demonstration(req_dict)


# ============================================================================
# ASSIGNMENT 5: Multi-Agent Negotiation Protocol
# ============================================================================
class NegotiationRequest(BaseModel):
    budget: float = 45000.0
    max_rounds: int = 3
    force_overage: bool = True


@app.post("/api/negotiation/run")
async def run_negotiation(request: NegotiationRequest):
    """Executes multi-turn negotiation bidding and consensus between Domain & Budget agents."""
    negotiator = MultiAgentNegotiator(max_rounds=request.max_rounds)
    return negotiator.run_negotiation(budget=request.budget, force_overage=request.force_overage)


# ============================================================================
# ASSIGNMENT 6: Utility Optimization (10 Travel Configurations)
# ============================================================================
class UtilityOptimizationRequest(BaseModel):
    budget: float = 45000.0
    destination: str = "Goa"


@app.post("/api/utility/optimize")
async def optimize_utility(request: UtilityOptimizationRequest):
    """Evaluates mathematical multi-attribute utility and ranks 10 travel configurations."""
    return run_utility_optimization(budget=request.budget, destination=request.destination)


# ============================================================================
# ASSIGNMENT 7: BDI Architecture & Dynamic Replanning
# ============================================================================
class BDIReplanRequest(BaseModel):
    budget: float = 40000.0
    shock_type: str = "price_surge"  # "price_surge" or "weather_disruption"


@app.post("/api/bdi/replan")
async def replan_bdi(request: BDIReplanRequest):
    """Demonstrates BDI Belief revision, Desire reconsideration, and Intention replanning."""
    return run_bdi_replanning_demonstration(budget=request.budget, shock_type=request.shock_type)


# ============================================================================
# ASSIGNMENT 8: Knowledge Base & Weather API Integration
# ============================================================================
@app.get("/api/knowledge/destinations")
async def list_destinations():
    """Lists destination profiles in the structured JSON ontology."""
    return list(DESTINATION_KNOWLEDGE_BASE.values())


@app.get("/api/knowledge/destination/{city}")
async def get_destination_knowledge(city: str):
    """Returns structured ontological profile for a specific destination."""
    return lookup_destination_knowledge(city)


@app.get("/api/weather/{city}")
async def get_weather(city: str):
    """Fetches real weather from Open-Meteo with high-fidelity mock fallback."""
    return fetch_weather_forecast(city)


# ============================================================================
# ASSIGNMENT 9: Cryptographic Security & Tamper Detection
# ============================================================================
@app.get("/api/security/audit")
async def run_security_audit():
    """Runs a multi-scenario cryptographic audit demonstrating legitimate vs tampered payloads."""
    return run_security_demonstration()


class VerifyMessageRequest(BaseModel):
    sender_id: str
    recipient_id: str
    timestamp: float
    nonce: str
    payload: Dict[str, Any]
    signature: str


@app.post("/api/security/verify")
async def verify_signed_message(request: VerifyMessageRequest):
    """Verifies HMAC-SHA256 signature and checks for tampering or replay."""
    msg = SignedMessage(**request.model_dump())
    result = _security_manager.verify_message(msg)
    return vars(result)


# ============================================================================
# ASSIGNMENT 10 & DEMO MODE: Capstone Integration
# ============================================================================
class CapstoneDemoRequest(BaseModel):
    origin: str = "DEL"
    destination: str = "Goa"
    budget: float = 45000.0
    traveler_type: str = "couple"
    interests: list[str] = Field(default_factory=lambda: ["beach", "culture", "relaxation"])


@app.post("/api/demo/run")
async def run_capstone_demo(request: Optional[CapstoneDemoRequest] = None):
    """
    Executes the end-to-end multi-agent lifecycle across all 10 modules:
    Rules -> Knowledge -> BDI -> Sockets -> Concurrency -> Negotiation ->
    Utility Optimization -> Security Audit -> Synthesis & Persistence.
    """
    args = request.model_dump() if request else {}
    return capstone_engine.run_full_lifecycle_demo(**args)


@app.get("/api/demo/history")
async def get_demo_history():
    """Returns past itineraries and demo executions saved in SQLite database."""
    return _store.list_all()


# ============================================================================
# Static Frontend Single-Page Application (SPA) Serving
# ============================================================================
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

_frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
_assets_dir = os.path.join(_frontend_dist, "assets")

if os.path.exists(_assets_dir):
    app.mount("/assets", StaticFiles(directory=_assets_dir), name="assets")


@app.get("/{full_path:path}")
async def serve_frontend_spa(full_path: str):
    # Do not intercept API or system endpoints
    if (
        full_path.startswith("api/")
        or full_path in ["health", "plan-trip", "trips"]
        or full_path.startswith("trips/")
    ):
        raise HTTPException(status_code=404, detail="Not Found")

    target_file = os.path.join(_frontend_dist, full_path)
    if os.path.exists(target_file) and os.path.isfile(target_file):
        return FileResponse(target_file)

    index_file = os.path.join(_frontend_dist, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)

    return {
        "service": "SmartTrip AI Multi-Agent Platform",
        "status": "OPERATIONAL",
        "version": "2.0.0",
        "dashboard": "Frontend build pending or running in API-only mode.",
    }
