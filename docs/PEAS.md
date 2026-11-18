# SmartTrip AI – PEAS Profile

| Element | Specification |
|---|---|
| Performance | Budget compliance, traveler preference fit, weather suitability, utility score, consensus completion, response latency |
| Environment | Dynamic and partially observable: destinations, fares, hotel inventory, weather conditions and traveler constraints |
| Actuators | Generated itinerary recommendations, negotiated flight/hotel/activity proposals, HMAC-signed TCP messages, SQLite execution history |
| Sensors | User form inputs, JSON knowledge base, live OpenWeather API or deterministic mock weather, budget calculations, worker telemetry |

## Environment Classification

- **Partially observable:** live inventory and all environmental outcomes are not known completely.
- **Stochastic:** fares, mock inventories and weather vary.
- **Sequential:** decisions depend on prior proposals, budget checks and replanning.
- **Dynamic:** weather and feasibility can change during execution.
- **Multi-agent:** flight, hotel, activity and budget agents exchange proposals.
- **Continuous ranking:** utility optimization ranks a finite set of candidate packages while costs and preferences vary.

## Agent vs. Object-Oriented Programming

An agent is an autonomous software entity with goals, state, perception and action behavior. An object is a class-based runtime structure that encapsulates data and methods but may remain passive. SmartTrip agents add ongoing status, proposal behavior, BDI state and negotiation responsibilities. The project combines both paradigms: agents are implemented with Python classes, state and dataclasses, while explicitly agent-oriented behavior is represented by rule evaluation, beliefs/desires/intentions, utility scoring and consensus coordination.
