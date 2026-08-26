import asyncio
from datetime import datetime
from backend.collectors.base_collector import BaseCollector

class LinuxSyslogCollector(BaseCollector):
    """
    Stub for a Syslog Receiver. In a real environment, this would listen on UDP 514.
    """
    def __init__(self, event_bus, port=514):
        super().__init__(event_bus)
        self.port = port

    async def collect(self):
        # As a stub, it just emits a fake heartbeat syslog every 30s
        while True:
            await asyncio.sleep(30)
            raw_event = {
                "collector_id": self.collector_id,
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": "SYSLOG_HEARTBEAT",
                "raw_message": "sshd[12345]: Server listening on 0.0.0.0 port 22.",
                "source_ip": "192.168.1.10",
                "destination_ip": "192.168.1.10",
                "hostname": "linux-server-01"
            }
            await self.event_bus.publish(raw_event)
