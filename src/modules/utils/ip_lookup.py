import logging
import urllib.request
import json
import socket
import re
from typing import List, Optional
from urllib.parse import urlparse
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)

class IpLookupModule(BaseModule):
    """Fetch and display local, public, and remote IP information"""

    def get_keyword(self) -> str:
        return "ip"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def _get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"

    def _fetch_ip_details(self, ip: str = "") -> dict:
        """Fetch IP details from ipapi.co. If ip is empty, fetches public IP details."""
        url_path = f"https://ipapi.co/{ip + '/' if ip else ''}json/"
        # Added User-Agent to avoid being blocked by API
        headers = {'User-Agent': 'uLauncher-OmniPack/1.0'}
        try:
            req = urllib.request.Request(url_path, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as url:
                return json.loads(url.read().decode())
        except Exception as e:
            logger.error(f"Failed to fetch IP details for '{ip}': {e}")
            return {}

    def _get_public_ip_fallback(self) -> Optional[str]:
        """Simple fallback to get just the public IP if detailed lookup fails."""
        try:
            headers = {'User-Agent': 'uLauncher-OmniPack/1.0'}
            req = urllib.request.Request("https://icanhazip.com", headers=headers)
            with urllib.request.urlopen(req, timeout=3) as url:
                return url.read().decode().strip()
        except Exception:
            return None

    def _is_valid_ip(self, ip: str) -> bool:
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def _resolve_domain(self, domain: str) -> Optional[str]:
        # Clean domain (remove protocol and paths)
        domain = domain.lower().strip()
        if domain.startswith(("http://", "https://")):
            domain = urlparse(domain).netloc
        elif "/" in domain:
            domain = domain.split("/")[0]
        
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            return None

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        query = query.strip()
        items = []

        # Case 1: My IP (Empty query or '?')
        if not query or query == "?":
            # 1. Local IP
            local_ip = self._get_local_ip()
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name=f"Local IP: {local_ip}",
                description="Your internal network IP. Press Enter to copy.",
                on_enter=CopyToClipboardAction(local_ip)
            ))

            # 2. Public IP Details
            details = self._fetch_ip_details()
            if details and "ip" in details:
                public_ip = details.get("ip")
                location = f"{details.get('city', '')}, {details.get('region', '')}, {details.get('country_name', '')}".strip(", ")
                org = details.get("org", "Unknown")
                items.append(ExtensionResultItem(
                    icon=self.get_icon(),
                    name=f"Public IP: {public_ip}",
                    description=f"Location: {location} | ISP: {org}",
                    on_enter=CopyToClipboardAction(public_ip)
                ))
            else:
                # Fallback to simple public IP
                public_ip = self._get_public_ip_fallback()
                if public_ip:
                    items.append(ExtensionResultItem(
                        icon=self.get_icon(),
                        name=f"Public IP: {public_ip}",
                        description="Fetched via fallback service. Press Enter to copy.",
                        on_enter=CopyToClipboardAction(public_ip)
                    ))
                else:
                    items.append(ExtensionResultItem(
                        icon=self.get_icon(),
                        name="Public IP: Error",
                        description="Could not fetch public IP information.",
                        on_enter=None
                    ))
            return items

        # Case 2: Query is an IP Address
        if self._is_valid_ip(query):
            details = self._fetch_ip_details(query)
            if details and "ip" in details:
                ip = details.get("ip", query)
                location = f"{details.get('city', '')}, {details.get('region', '')}, {details.get('country_name', '')}".strip(", ")
                org = details.get("org", "Unknown")
                items.append(ExtensionResultItem(
                    icon=self.get_icon(),
                    name=f"IP Details: {ip}",
                    description=f"Location: {location} | ASN/Org: {org}",
                    on_enter=CopyToClipboardAction(ip)
                ))
            else:
                items.append(ExtensionResultItem(
                    icon=self.get_icon(),
                    name=f"IP: {query}",
                    description="Could not fetch details for this IP.",
                    on_enter=CopyToClipboardAction(query)
                ))
            return items

        # Case 3: Query is a Domain
        target_ip = self._resolve_domain(query)
        if target_ip:
            details = self._fetch_ip_details(target_ip)
            if details and "ip" in details:
                location = f"{details.get('city', '')}, {details.get('region', '')}, {details.get('country_name', '')}".strip(", ")
                org = details.get("org", "Unknown")
                items.append(ExtensionResultItem(
                    icon=self.get_icon(),
                    name=f"Domain: {query} -> {target_ip}",
                    description=f"Location: {location} | ASN/Org: {org}",
                    on_enter=CopyToClipboardAction(target_ip)
                ))
            else:
                items.append(ExtensionResultItem(
                    icon=self.get_icon(),
                    name=f"Domain: {query} -> {target_ip}",
                    description="Press Enter to copy IP address.",
                    on_enter=CopyToClipboardAction(target_ip)
                ))
        else:
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name="Invalid input",
                description="Enter an IP, a domain (e.g. google.com), or '?' for your info.",
                on_enter=None
            ))

        return items
