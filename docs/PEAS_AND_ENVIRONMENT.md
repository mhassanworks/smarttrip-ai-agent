# SmartTrip AI — PEAS & Multi-Agent Environment Specification

## 1. PEAS Framework Specification

The PEAS (Performance Measure, Environment, Actuators, Sensors) model formalizes each autonomous agent operating within the SmartTrip AI architecture.

| Agent Persona | Performance Measure ($P$) | Environment ($E$) | Actuators ($A$) | Sensors ($S$) |
| :--- | :--- | :--- | :--- | :--- |
| **Flight Agent** | Cost within ceiling, minimal layovers/stops, convenient departure time, airline rating $\ge 4.0/5.0$ | Airline booking systems, fare cache, multi-tier pricing APIs (Amadeus, self-hosted fare dataset, mock generator) | Query flight APIs, rank candidate options, submit proposal to message log, emit floor-price flag | Origin, destination, departure date, flight budget ceiling, HTTP response codes |
| **Hotel Agent** | Nightly rate $\le$ ceiling, guest review score $\ge 4.0/5.0$, proximity to city center, amenity match | Hotel booking engines, room categories, city inventory, seasonal demand curves | Search lodging, room selection, cost-per-night calculation, reservation proposal generation | Destination city, check-in/out dates, guest count, accommodation budget ceiling |
| **Activity Agent** | Bundle cost $\le$ ceiling, diversity of attractions, interest match score, schedule feasibility | Landmark registries, monument entry fees (ASI fees, museum tickets), operating hours, weather forecasts | Itinerary curation, entry fee summation, activity pruning under budget pressure, daily scheduling | Traveler interests, trip duration, destination city, activity budget ceiling, weather conditions |
| **Pricing & Budget Arbiter** | Total cost $\le$ budget, minimal negotiation rounds, fair category allocation, variance minimization | Multi-agent message log, accumulated proposals, user financial ceiling, category ceilings | Budget variance evaluation, reallocation target flagging, ceiling adjustment signals, consensus authorization | Submitted proposals from Flight/Hotel/Activity agents, user max budget, negotiation round counter |
| **BDI Dynamic Planner** | Goal preservation rate under environmental shocks, replanning latency ($< 200\text{ ms}$), plan stability | Dynamic external world: airline fare surges, hotel sold-out events, weather disruptions | Belief revision, desire reconsideration, intention reconstruction, revised booking commitment | Real-time pricing feeds, cancellation alerts, weather warnings, user goal constraints |
| **TCP Socket Communication Agent** | Zero packet corruption, sub-millisecond serialization latency, successful handshake and mutual commit | TCP/IP network, stream sockets, JSON-serialized protocol frames | Socket bind/connect, length-delimited JSON frame transmission, acknowledgment dispatch, connection teardown | Socket buffer bytes, EOF signals, network latency timer, connection reset triggers |
| **Security & Verification Agent** | 100% detection of unauthorized or modified messages, 0 false acceptances, cryptographic overhead $< 5\text{ ms}$ | Inter-agent communication channel, potential hostile interceptors, untrusted endpoints | HMAC-SHA256 signature computation, sender identity validation, message quarantine/rejection, audit logging | Inbound payload bytes, cryptographic signatures, shared secret keys, nonce registry, timestamps |
| **Concurrency Telemetry Worker** | Zero race conditions, sub-millisecond lock wait times, continuous throughput under heavy loads | Multi-threaded Python execution runtime, job queues, shared metric memory buffers | Worker thread dispatch, queue push/pop, mutex lock acquisition/release, latency histogram updates | Queue depth counter, task completion ticks, CPU execution time, thread liveness flags |

---

## 2. Multi-Agent Environment Classification

Following Russell & Norvig's environment taxonomy:

1. **Observability: Partially Observable**  
   Agents do not possess omniscient global knowledge of all airline seats, dynamic hotel rates, or future weather. They must probe external endpoints and infer world state through selective queries.
2. **Determinism: Stochastic**  
   Prices, seat availability, weather conditions, and third-party API response times fluctuate probabilistically. Actions taken at time $t$ do not yield deterministic outcomes at $t+1$.
3. **Dynamism: Dynamic**  
   The environment evolves while agents deliberate: flight fares surge during high demand, hotel rooms sell out, and weather alerts arrive asynchronously.
4. **Continuity: Discrete turns with Continuous attributes**  
   Agents deliberate in discrete proposal rounds and communicate via discrete messages, but monetary budgets, latencies, and utility scores are continuous real numbers.
5. **Multi-Agent Structure: Cooperative & Competitive (Coopetitive)**  
   Agents share the overarching cooperative goal of constructing an optimal feasible trip, yet compete for finite budget allocations from the global expenditure pool.
6. **Episodic vs Sequential: Sequential**  
   Current decisions (e.g., flight chosen) directly constrain subsequent choices (e.g., hotel check-in time and remaining budget available for activities).

---

## 3. Autonomous Agents vs. Object-Oriented Programming (OOP)

| Dimension | Autonomous Multi-Agent Systems (MAS) | Object-Oriented Programming (OOP) |
| :--- | :--- | :--- |
| **Autonomy & Control** | **Active**: Retains internal control over whether and when to act. Evaluates percepts against goals before accepting or rejecting a proposal. | **Passive**: Encapsulates state, but delegates execution control to the caller. When a method is called, it executes unconditionally. |
| **Proactivity vs Reactivity** | **Goal-driven & proactive**: Takes initiative to optimize utility, monitor background prices, and trigger replanning when environmental beliefs change. | **Purely reactive**: Only executes code when invoked directly by an external thread or method caller. |
| **Interaction Model** | **Flexible communication**: Negotiates over shared communication channels (ACL, JSON sockets, LangGraph message logs) with bidding, counter-proposals, and consensus. | **Rigid method invocation**: Caller must know exact method signatures, argument types, and return values; tight temporal and semantic coupling. |
| **Environment Awareness** | **Situated in a dynamic environment**: Continuously updates internal beliefs via sensory feeds (weather, pricing) and actuates changes. | **Self-contained internal state**: Typically unaware of external environment unless passed as explicit parameters to method calls. |
| **Failure Handling & Resilience** | **Adaptive Replanning (BDI)**: Detects failure (e.g. over-budget, sold out) and autonomously searches for alternative recovery paths. | **Exception bubbling**: Raises exceptions up the call stack; relies on caller to catch or crashes execution flow. |
| **Design Objective** | **Utility maximization** under uncertainty and resource constraints. | **Data abstraction**, encapsulation, and code reuse through modular interfaces. |
