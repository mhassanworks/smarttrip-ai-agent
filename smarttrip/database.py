from __future__ import annotations
import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path

class TripDatabase:
    def __init__(self, path: Path):
        self.path = path
        self._init_db()

    def _connect(self):
        con = sqlite3.connect(self.path, timeout=10)
        con.row_factory = sqlite3.Row
        return con

    def _init_db(self):
        with self._connect() as con:
            con.executescript("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                origin TEXT,
                destination TEXT,
                budget REAL,
                status TEXT,
                summary_json TEXT
            );
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                event_type TEXT,
                agent_from TEXT,
                agent_to TEXT,
                detail TEXT
            );
            CREATE TABLE IF NOT EXISTS negotiation_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER,
                created_at TEXT NOT NULL,
                agent_name TEXT,
                action TEXT,
                detail TEXT
            );
            """)

    def save_run(self, origin, destination, budget, status, summary):
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO runs(created_at,origin,destination,budget,status,summary_json) VALUES(?,?,?,?,?,?)",
                (datetime.now(timezone.utc).isoformat(), origin, destination, budget, status,
                 json.dumps(summary, ensure_ascii=False)),
            )
            return cur.lastrowid

    def log_security(self, event_type, agent_from, agent_to, detail):
        with self._connect() as con:
            con.execute(
                "INSERT INTO security_events(created_at,event_type,agent_from,agent_to,detail) VALUES(?,?,?,?,?)",
                (datetime.now(timezone.utc).isoformat(), event_type, agent_from, agent_to, detail),
            )

    def log_negotiation(self, run_id, agent_name, action, detail):
        with self._connect() as con:
            con.execute(
                "INSERT INTO negotiation_events(run_id,created_at,agent_name,action,detail) VALUES(?,?,?,?,?)",
                (run_id, datetime.now(timezone.utc).isoformat(), agent_name, action, detail),
            )

    def fetch_all(self, table, limit=100):
        allowed = {"runs", "security_events", "negotiation_events"}
        if table not in allowed:
            raise ValueError("Invalid table")
        with self._connect() as con:
            rows = con.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]
