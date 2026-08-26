
import asyncio
import win32evtlog
import win32event
import win32con
from datetime import datetime
from backend.collectors.base_collector import BaseCollector

class WindowsCollector(BaseCollector):
    """
    Reads live Windows Security events and publishes them to the EventBus.
    """
    def __init__(self, event_bus, server="localhost", log_type="Security"):
        super().__init__(event_bus)
        self.server = server
        self.log_type = log_type

    async def collect(self):
        try:
            # We'll run this in a thread or just a loop since win32evtlog can block,
            # but for this prototype, we'll poll it asynchronously using asyncio.sleep
            try:
                hand = win32evtlog.OpenEventLog(self.server, self.log_type)
            except Exception as e:
                if "1314" in str(e) or "privilege" in str(e).lower():
                    print("\n[WARNING] Windows Collector: Administrator privileges required to read Security logs.")
                    print("          Live Windows logs will be disabled. Restart VSCode/Terminal as Admin to enable.\n")
                    return # Exit this collector task gracefully
                else:
                    raise e
                    
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            
            while True:
                events = win32evtlog.ReadEventLog(hand, flags, 0)
                if events:
                    for event in events:
                        # Convert event time
                        try:
                            ts = event.TimeGenerated.isoformat()
                        except:
                            ts = datetime.utcnow().isoformat()
                            
                        # Extremely basic parsing of Event ID
                        event_id = event.EventID & 0x1FFF # To get actual Event ID

                        # We'll map a few common ones
                        event_type = "WINDOWS_EVENT"
                        if event_id == 4624:
                            event_type = "SUCCESSFUL_LOGIN"
                        elif event_id == 4625:
                            event_type = "FAILED_LOGIN"

                        raw_event = {
                            "collector_id": self.collector_id,
                            "timestamp": ts,
                            "event_type": event_type,
                            "raw_message": f"Windows Event {event_id} from {event.SourceName}",
                            "source_ip": "127.0.0.1", # Hardcoded for now
                            "destination_ip": "localhost",
                            "hostname": event.ComputerName
                        }
                        await self.event_bus.publish(raw_event)
                
                await asyncio.sleep(5) # Poll every 5 seconds
                
        except Exception as e:
            print(f"Windows Collector Error: {e}")
