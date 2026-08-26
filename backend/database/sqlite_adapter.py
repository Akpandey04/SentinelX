import sqlite3
import json
from typing import List, Optional
from backend.database.storage_backend import StorageBackend
from backend.models.events import SentinelEvent, Severity, EventState
from backend.models.incidents import SentinelIncident, IncidentStatus

class SQLiteAdapter(StorageBackend):
    def __init__(self, db_path: str = "siem_data.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Events Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    schema_version TEXT,
                    event_version TEXT,
                    timestamp TEXT,
                    state TEXT,
                    raw_message TEXT,
                    collector_id TEXT,
                    hostname TEXT,
                    user TEXT,
                    source_ip TEXT,
                    destination_ip TEXT,
                    event_type TEXT,
                    action TEXT,
                    risk_score INTEGER,
                    severity TEXT,
                    tags TEXT,
                    metadata TEXT
                )
            ''')
            # Incidents Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS incidents (
                    incident_id TEXT PRIMARY KEY,
                    created_at TEXT,
                    updated_at TEXT,
                    title TEXT,
                    description TEXT,
                    status TEXT,
                    severity TEXT,
                    risk_score INTEGER,
                    related_events TEXT,
                    target_asset TEXT,
                    attacker_ip TEXT
                )
            ''')
            conn.commit()

    def save_event(self, event: SentinelEvent) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO events (
                    event_id, schema_version, event_version, timestamp, state, 
                    raw_message, collector_id, hostname, user, source_ip, 
                    destination_ip, event_type, action, risk_score, severity, 
                    tags, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event.event_id, event.schema_version, event.event_version, 
                event.timestamp.isoformat(), event.state.value, event.raw_message, 
                event.collector_id, event.hostname, event.user, event.source_ip, 
                event.destination_ip, event.event_type, event.action, event.risk_score, 
                event.severity.value if event.severity else None, 
                json.dumps(event.tags), json.dumps(event.metadata)
            ))
            conn.commit()

    def get_events(self, limit: int = 100) -> List[SentinelEvent]:
        # For this prototype, we'll return mock objects or raw dicts,
        # but properly we should parse them back to SentinelEvent.
        # This implementation can be fleshed out as needed.
        pass

    def save_incident(self, incident: SentinelIncident) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO incidents (
                    incident_id, created_at, updated_at, title, description,
                    status, severity, risk_score, related_events, target_asset, attacker_ip
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                incident.incident_id, incident.created_at.isoformat(), incident.updated_at.isoformat(),
                incident.title, incident.description, incident.status.value,
                incident.severity.value, incident.risk_score, json.dumps(incident.related_events),
                incident.target_asset, incident.attacker_ip
            ))
            conn.commit()

    def get_active_incident(self, attacker_ip: str, target_asset: str) -> Optional[SentinelIncident]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT incident_id, created_at, updated_at, title, description,
                       status, severity, risk_score, related_events, target_asset, attacker_ip
                FROM incidents
                WHERE attacker_ip = ? AND target_asset = ? AND status IN ('OPEN', 'INVESTIGATING')
                LIMIT 1
            ''', (attacker_ip, target_asset))
            row = cursor.fetchone()
            if row:
                # Need to properly deserialize
                from datetime import datetime
                return SentinelIncident(
                    incident_id=row[0],
                    created_at=datetime.fromisoformat(row[1]),
                    updated_at=datetime.fromisoformat(row[2]),
                    title=row[3],
                    description=row[4],
                    status=IncidentStatus(row[5]),
                    severity=Severity(row[6]),
                    risk_score=row[7],
                    related_events=json.loads(row[8]),
                    target_asset=row[9],
                    attacker_ip=row[10]
                )
            return None

    def get_incidents(self, limit: int = 100) -> List[SentinelIncident]:
        pass
