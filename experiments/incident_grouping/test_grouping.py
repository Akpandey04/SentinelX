import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.core.normalizer import SentinelEvent
from src.engines.incident import IncidentEngine
from src.database.sqlite_adapter import SQLiteAdapter
from src.models.events import EventState, Severity

def test_incident_boundary_separation():
    test_db = "test_incidents.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    adapter = SQLiteAdapter(test_db)
    
    engine = IncidentEngine(adapter)
    
    def make_ev(id, src, dst):
        return SentinelEvent(event_id=id, timestamp="2026-10-04T12:00:00Z", raw_message="m", collector_id="c", event_type="SSH_LOGIN_FAILED", source_ip=src, destination_ip=dst, state=EventState.DETECTED, risk_score=50, severity=Severity.HIGH)

    engine.process(make_ev("1", "10.0.0.1", "192.168.1.1"))
    engine.process(make_ev("2", "10.0.0.1", "192.168.1.1"))
    engine.process(make_ev("3", "10.0.0.2", "192.168.1.1"))
    engine.process(make_ev("4", "10.0.0.1", "192.168.1.2"))
    
    with adapter._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM incidents")
        count = cursor.fetchone()[0]
        
    assert count == 3
    if os.path.exists(test_db):
        os.remove(test_db)
