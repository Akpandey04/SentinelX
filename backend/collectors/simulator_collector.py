import asyncio
import yaml
import glob
import os
import random
from datetime import datetime
from backend.collectors.base_collector import BaseCollector

class SimulatorCollector(BaseCollector):
    """
    Simulates attacks by reading YAML profiles and publishing events.
    """
    def __init__(self, event_bus, profiles_dir="config/simulations/"):
        super().__init__(event_bus)
        self.profiles_dir = profiles_dir
        self.profiles = self._load_profiles()

    def _load_profiles(self):
        profiles = []
        pattern = os.path.join(self.profiles_dir, "*.yaml")
        for filepath in glob.glob(pattern):
            with open(filepath, 'r') as f:
                try:
                    profiles.append(yaml.safe_load(f))
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
        return profiles

    async def collect(self):
        # Create a task for each profile
        tasks = []
        for profile in self.profiles:
            tasks.append(asyncio.create_task(self._run_profile(profile)))
        
        # Also run a background noise generator
        tasks.append(asyncio.create_task(self._generate_noise()))
        
        await asyncio.gather(*tasks)

    async def _run_profile(self, profile: dict):
        freq = profile.get("frequency_seconds", 5)
        events = profile.get("events", [])
        if not events: return
        
        while True:
            await asyncio.sleep(freq)
            # Pick a random event from the profile
            evt_def = random.choice(events)
            
            raw_event = {
                "collector_id": self.collector_id,
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": evt_def.get("type", "UNKNOWN"),
                "raw_message": evt_def.get("message", ""),
                "source_ip": evt_def.get("source_ip", ""),
                "destination_ip": evt_def.get("target_asset", ""),
                "simulated_profile": profile.get("name", "Unknown")
            }
            await self.event_bus.publish(raw_event)

    async def _generate_noise(self):
        while True:
            await asyncio.sleep(2)
            raw_event = {
                "collector_id": self.collector_id,
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": "NETWORK_TRAFFIC",
                "raw_message": f"Allowed connection from {random.randint(1,255)}.{random.randint(1,255)}.1.1",
                "source_ip": f"{random.randint(1,255)}.{random.randint(1,255)}.1.1",
                "simulated_profile": "Background Noise"
            }
            await self.event_bus.publish(raw_event)
