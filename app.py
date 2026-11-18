from __future__ import annotations
import json
from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from smarttrip.config import DB_PATH, DATA_DIR, SOCKET_HOST, SOCKET_PORT
from smarttrip.database import TripDatabase
from smarttrip.knowledge import KnowledgeBase
from smarttrip.orchestrator import TravelOrchestrator
from smarttrip.socket_agent import AgentTCPServer, send_signed_message
from smarttrip.workers import BackgroundWorkerPool
from smarttrip.rules import TravelContext

st.set_page_config(page_title="SmartTrip AI", page_icon="✈", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
:root { --navy:#070D1A; --card:#111827; --line:#1F2937; --blue:#3B82F6; --cyan:#22D3EE; }
.stApp { background: radial-gradient(circle at top right, #101D35 0, #070D1A 38%, #050914 100%); }
[data-testid="stSidebar"] { background:#090F1E; border-right:1px solid #1F2937; }
.block-container { padding-top:1.6rem; max-width:1450px; }
.hero { padding:26px 30px; border:1px solid #1F2937; border-radius:18px;
        background:linear-gradient(135deg,rgba(59,130,246,.15),rgba(34,211,238,.05)); }
.hero h1 { margin:0; font-size:38px; letter-spacing:-1.5px; }
.hero p { color:#94A3B8; margin:8px 0 0; }
.card { background:rgba(17,24,39,.92); border:1px solid #1F2937; border-radius:14px;
        padding:18px; height:100%; box-shadow:0 12px 30px rgba(0,0,0,.12); }
.metric-label { color:#94A3B8; font-size:13px; text-transform:uppercase; letter-spacing:.08em; }
.metric-value { color:#F8FAFC; font-size:28px; font-weight:700; margin-top:4px; }
.status { display:inline-block; border-radius:999px; padding:5px 10px; font-size:12px;
          background:rgba(34,197,94,.12); color:#86EFAC; border:1px solid rgba(34,197,94,.25); }
.status.warn { background:rgba(245,158,11,.12); color:#FCD34D; border-color:rgba(245,158,11,.25); }
.small-muted { color:#94A3B8; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def create_services():
    db = TripDatabase(DB_PATH)
    kb = KnowledgeBase(DATA_DIR)
    orchestrator = TravelOrchestrator(kb)
    workers = BackgroundWorkerPool()
    server = AgentTCPServer(SOCKET_HOST, SOCKET_PORT, orchestrator.security)
    server.start()
    return db, kb, orchestrator, workers, server

db, kb, orchestrator, workers, tcp_server = create_services()

if "last_plan" not in st.session_state:
    st.session_state.last_plan = None
if "demo_count" not in st.session_state:
    st.session_state.demo_count = 0

with st.sidebar:
    st.markdown("### ✈ SmartTrip AI")
    st.markdown('<span class="status">● System operational</span>', unsafe_allow_html=True)
    st.caption("Autonomous Multi-Agent Travel Planner")
    page = st.radio("Workspace", [
        "Overview",
        "Travel Planner",
        "Agent Monitoring",
        "Negotiation Timeline",
        "Utility Optimization",
        "BDI State",
        "Knowledge Base",
        "Socket Communication",
        "Security Logs",
        "Background Workers",
    ], label_visibility="collapsed")
    st.divider()
    if st.button("▶ Run Complete Demo", use_container_width=True, type="primary"):
        destination = "Paris"
        plan = orchestrator.plan("New York", destination, str(date.today() + timedelta(days=30)),
                                 5, 6200, 2, "Culture")
        run_id = db.save_run(plan["origin"], destination, plan["budget"], "completed", plan)
        for event in plan["timeline"]:
            db.log_negotiation(run_id, event["agent"], event["action"], event["detail"])
        payload = {"sender": "Agent A", "receiver": "Agent B",
                   "destination": destination, "proposal": plan["best_package"]}
        signed = orchestrator.security.sign(payload)
        socket_result = send_signed_message(SOCKET_HOST, SOCKET_PORT, signed)
        tampered = signed.copy()
        tampered["payload"] = dict(tampered["payload"], destination="Unauthorized city")
        tampered_result = send_signed_message(SOCKET_HOST, SOCKET_PORT, tampered)
        db.log_security("signed_request", "Agent A", "Agent B",
                        f"Accepted: {socket_result.get('accepted')}")
        db.log_security("tampering_detected", "Agent A", "Agent B",
                        f"Rejected: {tampered_result.get('accepted')}")
        st.session_state.last_plan = plan
        st.session_state.demo_count += 1
        st.toast("Complete demo executed successfully", icon="✅")
    st.caption("Local runtime • HMAC-SHA256 • SQLite")

def card(title, value, subtitle=""):
    st.markdown(f'<div class="card"><div class="metric-label">{title}</div>'
                f'<div class="metric-value">{value}</div>'
                f'<div class="small-muted">{subtitle}</div></div>', unsafe_allow_html=True)

if page == "Overview":
    st.markdown('<div class="hero"><h1>SmartTrip AI</h1>'
                '<p>Autonomous multi-agent orchestration for intelligent travel planning</p></div>',
                unsafe_allow_html=True)
    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    runs = db.fetch_all("runs", 100)
    with c1: card("Total Plans", len(runs), "Persisted in SQLite")
    with c2: card("Active Agents", "5", "Flight • Hotel • Activity • Budget • Optimizer")
    with c3: card("Worker Threads", "2", f"{workers.monitor.snapshot()['count']} tasks processed")
    with c4: card("TCP Agent", "Online" if tcp_server.running else "Offline",
                  f"{SOCKET_HOST}:{SOCKET_PORT}")

    left, right = st.columns([1.25, 1])
    with left:
        st.subheader("System Architecture")
        nodes = [
            ("1", "User / Streamlit"), ("2", "Travel Orchestrator"),
            ("3", "Rules + BDI"), ("4", "Negotiating Agents"),
            ("5", "Utility Optimizer"), ("6", "Secure TCP Link"),
        ]
        html = '<div class="card">' + " → ".join(
            f'<span style="border:1px solid #334155;border-radius:8px;padding:8px 10px;'
            f'margin-right:6px;display:inline-block">{n}<br><b>{t}</b></span>'
            for n, t in nodes
        ) + "</div>"
        st.markdown(html, unsafe_allow_html=True)
    with right:
        st.subheader("Recent Execution")
        if runs:
            df = pd.DataFrame(runs)[["id", "created_at", "destination", "budget", "status"]]
            st.dataframe(df.head(8), use_container_width=True, hide_index=True)
        else:
            st.info("Run the complete demo to create the first execution.")

elif page == "Travel Planner":
    st.title("Travel Planner")
    with st.form("trip_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            origin = st.text_input("Origin", "New York")
            destination = st.selectbox("Destination", ["Paris", "Dubai", "Tokyo", "Bali", "Rome"])
        with c2:
            departure = st.date_input("Departure", date.today() + timedelta(days=30))
            days = st.slider("Trip duration", 2, 14, 5)
        with c3:
            budget = st.number_input("Budget (USD)", 800, 30000, 6200, 100)
            party_size = st.number_input("Travelers", 1, 8, 2)
        preference = st.radio("Travel style", ["Balanced", "Culture", "Adventure", "Relaxation", "Luxury"],
                              horizontal=True)
        submitted = st.form_submit_button("Generate Autonomous Plan", type="primary")
    if submitted:
        plan = orchestrator.plan(origin, destination, str(departure), days,
                                 float(budget), int(party_size), preference)
        st.session_state.last_plan = plan
        run_id = db.save_run(origin, destination, float(budget), "completed", plan)
        for event in plan["timeline"]:
            db.log_negotiation(run_id, event["agent"], event["action"], event["detail"])
        st.success("Plan generated and saved to SQLite.")

    plan = st.session_state.last_plan
    if plan:
        c1, c2, c3, c4 = st.columns(4)
        with c1: card("Estimated Cost", f"${plan['budget_status']['estimated_total']:,.0f}",
                      "Before final utility selection")
        with c2: card("Budget Remaining", f"${plan['budget_status']['remaining']:,.0f}",
                      "Consensus budget position")
        with c3: card("Weather", plan["weather"]["condition"],
                      f"{plan['weather']['temperature']}°C • {plan['weather']['source']}")
        with c4: card("Dynamic Replan", "Triggered" if plan["replanned"] else "Not needed",
                      "BDI reconfiguration")
        st.subheader("Recommended Package")
        best = plan["best_package"]
        st.markdown(f'<div class="card"><b>{best["name"]}</b> · Utility '
                    f'<span style="color:#22D3EE">{best["utility"]:.3f}</span><br>'
                    f'<span class="small-muted">Flight ${best["flight"]:,.0f} • Hotel '
                    f'${best["hotel"]:,.0f} • Activities ${best["activities"]:,.0f}</span></div>',
                    unsafe_allow_html=True)

elif page == "Agent Monitoring":
    st.title("Agent Monitoring")
    cols = st.columns(5)
    agents = [("Flight Agent", "Searching fares"), ("Hotel Agent", "Comparing stays"),
              ("Activity Agent", "Matching preferences"), ("Budget Agent", "Checking constraints"),
              ("Utility Agent", "Ranking packages")]
    for col, (name, action) in zip(cols, agents):
        with col:
            st.markdown(f'<div class="card"><div class="metric-label">{name}</div>'
                        f'<div class="metric-value">●</div><div class="small-muted">{action}</div></div>',
                        unsafe_allow_html=True)
    st.subheader("Agent Execution Status")
    plan = st.session_state.last_plan
    if plan:
        status_rows = [
            ["Flight", plan["flight"]["carrier"], "Complete", plan["flight"]["airfare"]],
            ["Hotel", f"{plan['hotel']['stars']}-star", "Complete", plan["hotel"]["nightly_rate"]],
            ["Activity", ", ".join(plan["activities"]["items"][:2]), "Complete",
             plan["activities"]["total_cost"]],
            ["Budget", "Consensus" if plan["budget_status"]["within_budget"] else "Replanning",
             "Complete", plan["budget_status"]["estimated_total"]],
        ]
        st.dataframe(pd.DataFrame(status_rows, columns=["Agent", "Proposal", "Status", "Cost"]),
                     use_container_width=True, hide_index=True)
    else:
        st.info("Generate a plan to populate live agent status.")

elif page == "Negotiation Timeline":
    st.title("Negotiation Timeline")
    plan = st.session_state.last_plan
    if not plan:
        st.info("Generate a travel plan or run the demo.")
    else:
        for event in plan["timeline"]:
            st.markdown(f'<div class="card" style="margin-bottom:10px"><b>Round {event["round"]} · '
                        f'{event["agent"]}</b><br><span class="small-muted">{event["action"]}: '
                        f'{event["detail"]}</span></div>', unsafe_allow_html=True)

elif page == "Utility Optimization":
    st.title("Utility Optimization")
    plan = st.session_state.last_plan
    if not plan:
        st.info("Generate a travel plan to rank 10 packages.")
    else:
        df = pd.DataFrame(plan["packages"])
        fig = px.bar(df, x="package_id", y="utility", color="utility",
                     title="Utility score ranking across 10 travel packages",
                     labels={"package_id": "Package", "utility": "Utility"},
                     color_continuous_scale=["#2563EB", "#22D3EE"])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(17,24,39,.6)", height=420)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df[["package_id", "name", "flight", "hotel", "activities",
                         "preference_score", "comfort_score", "weather_score", "utility"]]
                     .sort_values("utility", ascending=False),
                     use_container_width=True, hide_index=True)

elif page == "BDI State":
    st.title("BDI State Monitor")
    plan = st.session_state.last_plan
    if not plan:
        st.info("Generate a travel plan to inspect beliefs, desires and intentions.")
    else:
        bdi = plan["bdi"]
        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader("Beliefs")
            st.json(bdi["beliefs"])
        with c2:
            st.subheader("Desires")
            for desire in bdi["desires"]: st.markdown(f"• {desire}")
        with c3:
            st.subheader("Intentions")
            for intention in bdi["intentions"]: st.markdown(f"• {intention}")

elif page == "Knowledge Base":
    st.title("Knowledge Base")
    c1, c2 = st.columns([1, 2])
    with c1:
        selected = st.selectbox("Destination", list(kb.data["destinations"]))
        if st.button("Refresh live weather"):
            weather = kb.weather(selected)
            st.session_state.weather_preview = weather
        if "weather_preview" not in st.session_state:
            st.session_state.weather_preview = kb.weather(selected)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(st.session_state.weather_preview)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.subheader("JSON Knowledge Representation")
        st.json(kb.data)

elif page == "Socket Communication":
    st.title("TCP Socket Communication")
    c1, c2 = st.columns(2)
    with c1:
        card("Transport", "TCP/IP", f"{SOCKET_HOST}:{SOCKET_PORT}")
    with c2:
        card("Protocol", "JSON + HMAC", "Agent A → Agent B")
    st.subheader("Server Message Log")
    if tcp_server.log:
        for entry in reversed(tcp_server.log[-20:]):
            st.markdown(f'<div class="card" style="margin-bottom:8px"><b>{entry["status"]}</b>'
                        f' · {entry["direction"]}<br><code>{json.dumps(entry["response"])}</code></div>',
                        unsafe_allow_html=True)
    else:
        st.info("No socket messages yet. Run the complete demo.")

elif page == "Security Logs":
    st.title("Security Logs")
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("Verify HMAC with a test message"):
            envelope = orchestrator.security.sign({"test": "authenticated"})
            db.log_security("hmac_test", "Agent A", "Agent B",
                            f"Verified={orchestrator.security.verify(envelope)}")
            st.success("Signed and verified.")
    with c2:
        events = db.fetch_all("security_events", 100)
        if events:
            st.dataframe(pd.DataFrame(events)[["id", "created_at", "event_type", "agent_from",
                                               "agent_to", "detail"]],
                         use_container_width=True, hide_index=True)
        else:
            st.info("No security events recorded.")

elif page == "Background Workers":
    st.title("Background Worker Monitoring")
    snapshot = workers.monitor.snapshot()
    c1, c2, c3 = st.columns(3)
    with c1: card("Completed Tasks", snapshot["count"], "Across two daemon workers")
    with c2: card("Average Latency", f"{snapshot['average_ms']} ms", "Thread execution latency")
    with c3: card("Maximum Latency", f"{snapshot['max_ms']} ms", "Slowest sampled task")

    if st.button("Submit sample background task"):
        workers.submit("weather-benchmark",
                       lambda: kb.weather(st.session_state.get("worker_destination", "Tokyo")))
        st.toast("Background task queued", icon="⚙")

    completed = workers.drain()
    if completed:
        st.dataframe(pd.DataFrame(completed), use_container_width=True, hide_index=True)
    if snapshot["samples"]:
        fig = px.line(y=snapshot["samples"], title="Recent worker latency samples",
                      labels={"x": "Sample", "y": "Milliseconds"})
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(17,24,39,.6)")
        st.plotly_chart(fig, use_container_width=True)
