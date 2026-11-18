"""
Assignment 1: PEAS & Environment Module

Formal specification of agent personas, PEAS matrices (Performance measure,
Environment, Actuators, Sensors), environment taxonomy, and comparison
between Autonomous Multi-Agent Systems and Object-Oriented Programming (OOP).
"""
from typing import Any, Dict, List

PEAS_MATRIX: List[Dict[str, Any]] = [
    {
        "agent": "Flight Agent",
        "role": "Autonomous Airline Search & Fare Optimization",
        "performance_measure": "Cost within ceiling, minimal layovers/stops, convenient departure time, airline reliability rating >= 4.0",
        "environment": "Airline inventories, multi-tier pricing APIs (Amadeus, private data service, mock), flight schedules, seat classes",
        "actuators": "API queries, flight option ranking, proposal submission to message bus, floor-price flag emission",
        "sensors": "Trip request (origin, destination, departure date), category budget ceiling, HTTP response codes, latency metrics",
        "characteristics": ["Goal-directed", "Utility-driven", "Fall-through resilient"],
    },
    {
        "agent": "Hotel Agent",
        "role": "Lodging Acquisition & Amenity Alignment",
        "performance_measure": "Nightly rate <= ceiling, guest review score >= 4.0/5.0, proximity to attractions, cancellation flexibility",
        "environment": "Hotel booking systems, room inventory, location coordinates, seasonal demand curves",
        "actuators": "Hotel search execution, room selection, cost-per-night calculation, reservation proposal generation",
        "sensors": "Destination city, check-in/out dates, guest count, accommodation budget ceiling",
        "characteristics": ["Constraint-satisfying", "Preference-aware", "Negotiating"],
    },
    {
        "agent": "Activity Agent",
        "role": "Experience Curation & Attraction Scheduling",
        "performance_measure": "Activity bundle cost <= ceiling, diversity of cultural/leisure experiences, interest match score, schedule feasibility",
        "environment": "Landmark registries, monument entry fees (ASI fees, museum tickets), operating hours, weather forecasts",
        "actuators": "Itinerary curation, entry fee summation, activity pruning under budget pressure, day-by-day scheduling",
        "sensors": "Traveler interests, trip duration, destination city, activity budget ceiling, weather conditions",
        "characteristics": ["Context-aware", "Content-filtering", "Adaptive"],
    },
    {
        "agent": "Pricing & Budget Agent",
        "role": "Financial Arbitration & Consensus Arbiter",
        "performance_measure": "Total itinerary cost <= user budget, minimal negotiation rounds, fair category allocation, variance minimization",
        "environment": "Multi-agent message log, accumulated proposals, user financial ceiling, category ceilings",
        "actuators": "Budget variance evaluation, reallocation target flagging, ceiling adjustment signals, consensus authorization",
        "sensors": "Submitted proposals from Flight/Hotel/Activity agents, user max budget, negotiation round counter",
        "characteristics": ["Arbitrating", "Cooperative", "Convergence-optimizing"],
    },
    {
        "agent": "BDI Planner Agent",
        "role": "Dynamic Belief-Desire-Intention Replanning",
        "performance_measure": "Goal preservation rate under environmental shocks, replanning latency (< 200ms), plan stability",
        "environment": "Dynamic external world: airline fare surges, hotel sold-out events, weather disruptions",
        "actuators": "Belief revision, desire reconsideration, intention reconstruction, revised booking commitment",
        "sensors": "Real-time pricing feeds, cancellation alerts, weather warnings, user goal constraints",
        "characteristics": ["Proactive", "Reactive", "Self-healing"],
    },
    {
        "agent": "Socket Communication Agent",
        "role": "Low-Latency Inter-Agent TCP Messaging",
        "performance_measure": "Zero packet corruption, sub-millisecond serialization latency, successful handshake and mutual commit",
        "environment": "TCP/IP local/distributed network, stream sockets, JSON-serialized protocol frames",
        "actuators": "Socket bind/connect, length-delimited JSON frame transmission, acknowledgment dispatch, connection teardown",
        "sensors": "Socket buffer bytes, EOF signals, network latency timer, connection reset triggers",
        "characteristics": ["Deterministic", "Protocol-compliant", "Synchronous/Asynchronous"],
    },
    {
        "agent": "Security & Verification Agent",
        "role": "Cryptographic Authenticity & Tamper Detection",
        "performance_measure": "100% detection of unauthorized or modified messages, 0 false acceptances, cryptographic overhead < 5ms",
        "environment": "Inter-agent communication channel, potential hostile interceptors, untrusted endpoints",
        "actuators": "HMAC-SHA256 signature computation, sender identity validation, message quarantine/rejection, security audit logging",
        "sensors": "Inbound payload bytes, cryptographic signatures, shared secret keys, nonce registry, timestamps",
        "characteristics": ["Guarding", "Non-repudiating", "Zero-trust"],
    },
    {
        "agent": "Concurrency Monitoring Worker",
        "role": "Thread-Safe Background Telemetry & Health Checks",
        "performance_measure": "Zero race conditions, sub-millisecond lock wait times, continuous throughput under heavy loads",
        "environment": "Multi-threaded Python execution runtime, job queues, shared metric memory buffers",
        "actuators": "Worker thread dispatch, queue push/pop, mutex lock acquisition/release, latency histogram updates",
        "sensors": "Queue depth counter, task completion ticks, CPU execution time, thread liveness flags",
        "characteristics": ["Concurrent", "Thread-safe", "Telemetry-driven"],
    },
]

ENVIRONMENT_CLASSIFICATIONS: List[Dict[str, Any]] = [
    {
        "dimension": "Observability",
        "classification": "Partially Observable",
        "justification": "Agents do not have full global knowledge of all airline seats, dynamic hotel rates, or future weather. They must probe external APIs and infer state through selective queries.",
    },
    {
        "dimension": "Determinism",
        "classification": "Stochastic",
        "justification": "Prices, availability, weather, and third-party API response times fluctuate probabilistically. Actions (e.g. attempting to book at a price) have non-deterministic outcomes over time.",
    },
    {
        "dimension": "Dynamism",
        "classification": "Dynamic",
        "justification": "The environment evolves while agents deliberate: flight fares surge during high demand, hotel rooms sell out, and weather alerts arrive asynchronously.",
    },
    {
        "dimension": "Continuity",
        "classification": "Discrete turns with Continuous attributes",
        "justification": "Agents negotiate in discrete proposal rounds and communicate via discrete messages, but monetary budgets, latencies, and utility scores are continuous real numbers.",
    },
    {
        "dimension": "Multi-Agent Structure",
        "classification": "Cooperative & Competitive (Coopetitive)",
        "justification": "Agents share the overarching cooperative goal of constructing an optimal feasible trip, yet compete for finite budget allocations from the global expenditure pool.",
    },
    {
        "dimension": "Episodic vs Sequential",
        "classification": "Sequential",
        "justification": "Current decisions (e.g., flight chosen) directly constrain subsequent choices (e.g., hotel check-in time and remaining budget available for activities).",
    },
]

AGENT_VS_OOP_COMPARISON: List[Dict[str, Any]] = [
    {
        "dimension": "Autonomy & Control",
        "autonomous_agent": "Active: Retains internal control over whether and when to act. Evaluates percepts against goals before accepting or rejecting a proposal.",
        "oop_object": "Passive: Encapsulates state, but delegates execution control to the caller. When a method is called, it executes blindly without self-determination.",
    },
    {
        "dimension": "Proactivity vs Reactivity",
        "autonomous_agent": "Goal-driven and proactive: Takes initiative to optimize utility, monitor background prices, and trigger replanning when environmental beliefs change.",
        "oop_object": "Purely reactive: Only executes code when invoked directly by an external thread or method caller.",
    },
    {
        "dimension": "Interaction Model",
        "autonomous_agent": "Flexible communication: Negotiates over shared communication channels (ACL, JSON sockets, LangGraph message logs) with bidding, counter-proposals, and consensus.",
        "oop_object": "Rigid method invocation: Caller must know exact method signatures, argument types, and return values; tight temporal and semantic coupling.",
    },
    {
        "dimension": "Environment Awareness",
        "autonomous_agent": "Situated in a dynamic environment: Continuously updates internal beliefs via sensory feeds (weather, pricing) and actuates changes.",
        "oop_object": "Self-contained internal state: Typically unaware of external environment unless passed as explicit parameters to method calls.",
    },
    {
        "dimension": "Failure Handling & Resilience",
        "autonomous_agent": "Adaptive Replanning (BDI): Detects failure (e.g. over-budget, sold out) and autonomously searches for alternative recovery paths.",
        "oop_object": "Exception bubbling: Raises exceptions up the call stack; relies on caller to catch or crashes execution flow.",
    },
    {
        "dimension": "Design Objective",
        "autonomous_agent": "Utility maximization under uncertainty and resource constraints.",
        "oop_object": "Data abstraction, encapsulation, and code reuse through modular interfaces.",
    },
]


def get_peas_documentation() -> Dict[str, Any]:
    """Returns the complete PEAS and environment specification."""
    return {
        "title": "SmartTrip AI — PEAS & Multi-Agent Environment Specification",
        "version": "2.0.0",
        "peas_matrix": PEAS_MATRIX,
        "environment_classifications": ENVIRONMENT_CLASSIFICATIONS,
        "agent_vs_oop": AGENT_VS_OOP_COMPARISON,
    }
