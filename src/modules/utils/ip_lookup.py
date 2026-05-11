import logging
import urllib.request
import json
import socket
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)

class IpLookupModule(BaseModule):
    """Fetch and display local and public IP information"""

    def get_keyword(self) -> str:
        return "ip"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        items = []
        
        # 1. Local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name=f"Local IP: {local_ip}",
                description="Your internal network IP. Press Enter to copy.",
                on_enter=CopyToClipboardAction(local_ip)
            ))
        except Exception as e:
            logger.error(f"Failed to get local IP: {e}")

        # 2. Public IP & Geolocation
        try:
            # We'll use ipapi.co for detailed info (no API key needed for basic usage)
            with urllib.request.urlopen("https://ipapi.co/json/", timeout=3) as url:
                data = json.loads(url.read().decode())
                
                public_ip = data.get("ip", "Unknown")
                city = data.get("city", "")
                region = data.get("region", "")
                country = data.get("country_name", "")
                org = data.get("org", "Unknown")
                
                location = f"{city}, {region}, {country}".strip(", ")
                
                items.append(ExtensionResultItem(
                    icon=self.get_icon(),
                    name=f"Public IP: {public_ip}",
                    description=f"Location: {location} | ISP: {org}",
                    on_enter=CopyToClipboardAction(public_ip)
                ))
                
                if location:
                    items.append(ExtensionResultItem(
                        icon=self.get_icon(),
                        name=f"Location: {location}",
                        description="Based on your public IP. Press Enter to copy.",
                        on_enter=CopyToClipboardAction(location)
                    ))
        except Exception as e:
            logger.debug(f"Public IP fetch failed: {e}")
            # Fallback to simpler service if ipapi.co fails
            try:
                with urllib.request.urlopen("https://icanhazip.com", timeout=2) as url:
                    public_ip = url.read().decode().strip()
                    items.append(ExtensionResultItem(
                        icon=self.get_icon(),
                        name=f"Public IP: {public_ip}",
                        description="Press Enter to copy.",
                        on_enter=CopyToClipboardAction(public_ip)
                    ))
            except Exception as e2:
                logger.error(f"Fallback public IP fetch failed: {e2}")
                items.append(ExtensionResultItem(
                    icon=self.get_icon(),
                    name="Public IP: Error",
                    description="Could not fetch public IP information.",
                    on_enter=None
                ))

        return items
