import asyncio
import json
import os
from datetime import datetime

class IOCUpdater:
    """
    Periodically fetches Threat Intelligence feeds and updates local IOC lists.
    """
    def __init__(self, ioc_dir="config/ioc/"):
        self.ioc_dir = ioc_dir
        if not os.path.exists(self.ioc_dir):
            os.makedirs(self.ioc_dir)

    async def start(self):
        print("IOC Updater Service Started.")
        while True:
            try:
                # In a real scenario, this would make an HTTP request to AlienVault OTX
                # or a similar threat feed API. We simulate the update here.
                malicious_ips = ["198.51.100.44", "203.0.113.15", "185.20.11.3"]
                data = {
                    "last_updated": datetime.utcnow().isoformat(),
                    "indicators": {
                        "ipv4": malicious_ips,
                        "domains": ["evil-c2-server.com"]
                    }
                }
                
                filepath = os.path.join(self.ioc_dir, "feed.json")
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
                    
                print(f"IOC Feeds updated at {data['last_updated']}")
            except Exception as e:
                print(f"Error updating IOC feeds: {e}")
                
            await asyncio.sleep(3600) # Update every hour
