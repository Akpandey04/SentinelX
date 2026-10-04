from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

class EventState(str, Enum):
    NEW = "NEW"
    NORMALIZED = "NORMALIZED"
    DETECTED = "DETECTED"
    CORRELATED = "CORRELATED"
    INCIDENT = "INCIDENT"
    NOTIFIED = "NOTIFIED"
    CLOSED = "CLOSED"

class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class SentinelEvent(BaseModel):
    schema_version: str = "1.0"
    event_version: str = "1.0"
    event_id: str = Field(default_factory=lambda: f"EVT-{uuid.uuid4().hex[:8].upper()}")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    state: EventState = EventState.NEW
    
    # Raw log data
    raw_message: str
    collector_id: str
    
    # Normalized fields (Populated by Normalizer)
    hostname: Optional[str] = None
    user: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    event_type: Optional[str] = None
    action: Optional[str] = None
    
    # Risk and Enrichment (Populated by IOC/Risk Engines)
    risk_score: int = 0
    severity: Optional[Severity] = None
    tags: List[str] = Field(default_factory=list)
    
    # Flexible metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
