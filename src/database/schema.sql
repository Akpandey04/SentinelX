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
);

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
    attacker_ip TEXT,
    tags TEXT
);