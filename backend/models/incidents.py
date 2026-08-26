from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid
from backend.models.events import Severity

class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class SentinelIncident(BaseModel):
    incident_id: str = Field(default_factory=lambda: f"INC-{uuid.uuid4().hex[:8].upper()}")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    title: str
    description: str
    
    # State tracking
    status: IncidentStatus = IncidentStatus.OPEN
    severity: Severity = Severity.LOW
    risk_score: int = 0
    
    # Aggregation
    related_events: List[str] = Field(default_factory=list) # List of event_ids
    
    # Context
    target_asset: Optional[str] = None
    attacker_ip: Optional[str] = None
