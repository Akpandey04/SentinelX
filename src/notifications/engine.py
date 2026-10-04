import os
import datetime
from src.models.events import SentinelEvent, EventState
from src.reporting.reporting import generate_pdf_report
from src.reporting.mailer import send_alerts_to_list

class NotificationEngine:
    def __init__(self):
        # Create reports directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)

    def notify(self, event: SentinelEvent):
        """
        Logs the incident to the Notification Engine. 
        Emails will be batched and sent via the Scheduler service.
        """
        if event.state == EventState.INCIDENT:
            incident_id = event.metadata.get('incident_id', 'UNKNOWN')
            print(f"[NOTIFICATION ENGINE] Incident {incident_id} recorded. Scheduled for next email batch.")
