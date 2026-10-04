import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.core.normalizer import SentinelEvent
from src.engines.incident import IncidentEngine
from src.database.sqlite_adapter import SQLiteAdapter
from src.models.events import EventState, Severity

def run_aar_validation(alerts_count):
    test_db = "test_aar.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    adapter = SQLiteAdapter(test_db)
    
    engine = IncidentEngine(adapter)
    
    for i in range(alerts_count):
        e = SentinelEvent(event_id=str(i), timestamp="2026-10-04T12:00:00Z", raw_message="msg", collector_id="c", event_type="SSH_LOGIN_FAILED", source_ip="198.51.100.44", destination_ip="web-server-01", state=EventState.DETECTED, risk_score=50, severity=Severity.HIGH)
        engine.process(e)
        
    with adapter._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM incidents")
        incidents_count = cursor.fetchone()[0]
        
    aar = (1 - (incidents_count / alerts_count)) * 100
    print(f"{alerts_count} Alerts -> {incidents_count} Incident(s) (AAR = {aar:.2f}%)")
    
    if os.path.exists(test_db):
        os.remove(test_db)

if __name__ == "__main__":
    run_aar_validation(206)
