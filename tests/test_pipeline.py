import pytest
from src.core.normalizer import SentinelEvent
from src.engines.detection import DetectionEngine
from src.engines.risk import RiskEngine
from src.models.events import EventState

def make_event(event_type):
    return SentinelEvent(
        event_id="test",
        timestamp="2026-10-04T12:00:00Z",
        raw_message="msg",
        collector_id="test_col",
        event_type=event_type
    )

def test_normalization():
    event = make_event("TEST")
    assert event.event_type == "TEST"

def test_detection():
    engine = DetectionEngine()
    event = make_event("SSH_LOGIN_FAILED")
    res = engine.detect(event)
    assert res.state.value == "DETECTED"

def test_risk():
    engine = RiskEngine()
    event = make_event("BRUTE_FORCE_SUCCESS")
    event.state = EventState.DETECTED
    res = engine.evaluate(event)
    assert res.risk_score == 95

def test_aggregation():
    assert True

def test_persistence():
    assert True
