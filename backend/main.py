import asyncio
import uvicorn
from backend.api.server import app
from backend.core.event_bus import EventBus
from backend.core.pipeline_manager import PipelineManager
from backend.database.sqlite_adapter import SQLiteAdapter
from backend.collectors.simulator_collector import SimulatorCollector
from backend.collectors.windows_collector import WindowsCollector
from backend.collectors.linux_collector import LinuxSyslogCollector
from backend.collectors.wazuh_collector import WazuhCollector
from backend.core.ioc_updater import IOCUpdater

event_bus = EventBus()
storage = SQLiteAdapter()
pipeline = PipelineManager(event_bus, storage)

# Initialize all collectors and services
simulator = SimulatorCollector(event_bus)
windows = WindowsCollector(event_bus)
linux = LinuxSyslogCollector(event_bus)
wazuh = WazuhCollector(event_bus)
ioc_updater = IOCUpdater()

@app.on_event("startup")
async def startup_event():
    # Start the pipeline manager
    asyncio.create_task(pipeline.run())
    
    # Start all background tasks
    asyncio.create_task(simulator.collect())
    asyncio.create_task(windows.collect())
    asyncio.create_task(linux.collect())
    asyncio.create_task(wazuh.collect())
    asyncio.create_task(ioc_updater.start())
    
    print("SentinelX System Started.")

def main():
    print("Starting SentinelX Backend API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()