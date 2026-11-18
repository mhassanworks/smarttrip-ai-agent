from pathlib import Path
import tempfile

from smarttrip.database import TripDatabase
from smarttrip.knowledge import KnowledgeBase
from smarttrip.orchestrator import TravelOrchestrator
from smarttrip.rules import ConditionActionEngine, TravelContext
from smarttrip.security import HMACSecurity
from smarttrip.utility import rank_packages


def test_rule_engine_produces_actions():
    engine = ConditionActionEngine()
    result = engine.evaluate(TravelContext(3000, 2, "Light rain", "Culture", 5))
    assert len(result["actions"]) >= 3
    assert result["per_person_budget"] == 1500


def test_hmac_accepts_valid_and_rejects_tampered():
    security = HMACSecurity("test-secret")
    signed = security.sign({"destination": "Paris"})
    assert security.verify(signed)
    signed["payload"]["destination"] = "Tokyo"
    assert not security.verify(signed)


def test_end_to_end_plan_has_consensus_and_packages():
    with tempfile.TemporaryDirectory() as temp:
        kb = KnowledgeBase(Path(temp))
        orchestrator = TravelOrchestrator(kb)
        plan = orchestrator.plan("New York", "Paris", "2026-12-01", 5, 6200, 2, "Culture")
        assert plan["destination"] == "Paris"
        assert len(plan["timeline"]) >= 5
        assert len(plan["packages"]) == 10
        assert plan["best_package"]["utility"] >= plan["packages"][-1]["utility"]


def test_database_persistence():
    with tempfile.TemporaryDirectory() as temp:
        db = TripDatabase(Path(temp) / "test.db")
        run_id = db.save_run("NYC", "Paris", 6200, "completed", {"ok": True})
        db.log_security("test", "A", "B", "verified")
        assert run_id > 0
        assert len(db.fetch_all("runs")) == 1
        assert len(db.fetch_all("security_events")) == 1


def test_utility_ranking_is_deterministic_and_sorted():
    first = rank_packages("Paris", 5, 6200, "Culture", "Clear skies", 2)
    second = rank_packages("Paris", 5, 6200, "Culture", "Clear skies", 2)
    assert [p.package_id for p in first] == [p.package_id for p in second]
    scores = [p.utility for p in first]
    assert scores == sorted(scores, reverse=True)
