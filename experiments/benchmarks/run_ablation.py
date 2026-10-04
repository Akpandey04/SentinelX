import asyncio
import os
import csv
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.events import SentinelEvent, EventState, Severity
from src.database.sqlite_adapter import SQLiteAdapter
from src.engines.incident import IncidentEngine

def run_grouping_tests():
    print("Running Incident Grouping Correctness Tests...")
    db_path = "test_grouping.db"
    if os.path.exists(db_path): os.remove(db_path)
    
    storage = SQLiteAdapter(db_path)
    engine = IncidentEngine(storage)
    
    # Test Cases
    events = [
        # Case 1: Attacker A -> Target X
        SentinelEvent(raw_message="", collector_id="T1", source_ip="1.1.1.1", destination_ip="10.0.0.1", state=EventState.DETECTED, severity=Severity.HIGH, risk_score=50),
        # Case 2: Attacker A -> Target X (Should group with Case 1)
        SentinelEvent(raw_message="", collector_id="T2", source_ip="1.1.1.1", destination_ip="10.0.0.1", state=EventState.DETECTED, severity=Severity.HIGH, risk_score=50),
        # Case 3: Attacker B -> Target X (Different attacker, same target -> New Incident)
        SentinelEvent(raw_message="", collector_id="T3", source_ip="2.2.2.2", destination_ip="10.0.0.1", state=EventState.DETECTED, severity=Severity.HIGH, risk_score=50),
        # Case 4: Attacker A -> Target Y (Same attacker, different target -> New Incident)
        SentinelEvent(raw_message="", collector_id="T4", source_ip="1.1.1.1", destination_ip="10.0.0.2", state=EventState.DETECTED, severity=Severity.HIGH, risk_score=50),
    ]

    for e in events:
        engine.process(e)
        
    # Verify in DB
    import sqlite3
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT incident_id, attacker_ip, target_asset, related_events FROM incidents")
    incidents = c.fetchall()
    
    results = []
    print(f"Total Incidents Created: {len(incidents)} (Expected: 3)")
    for inc in incidents:
        import json
        rel = json.loads(inc[3])
        print(f"Incident {inc[0][:8]} | Attacker: {inc[1]} | Target: {inc[2]} | Alert Count: {len(rel)}")
        results.append({
            "incident_id": inc[0],
            "attacker_ip": inc[1],
            "target_asset": inc[2],
            "alert_count": len(rel)
        })
        
    # Calculate AAR for this tiny batch
    detected = len(events)
    created = len(incidents)
    aar = (1 - (created / detected)) * 100
    print(f"Aggregation Ratio for Test Batch: {aar:.2f}%\n")
    
    with open("incident_grouping_tests.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["incident_id", "attacker_ip", "target_asset", "alert_count"])
        writer.writeheader()
        writer.writerows(results)

    conn.close()
    if hasattr(storage, 'conn'):
        storage.conn.close()
    os.remove(db_path)

if __name__ == "__main__":
    run_grouping_tests()