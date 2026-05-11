import logging
import subprocess
import os
import signal
import shutil
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)

class KillPortModule(BaseModule):
    """Kill process listening on a specific port"""

    def get_keyword(self) -> str:
        return "port"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        if not shutil.which("lsof"):
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="lsof not found",
                description="Please install 'lsof' to use the port killer module",
                on_enter=HideWindowAction()
            )]

        query = query.strip()
        all_ports = self.get_open_ports()

        if not all_ports:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="No active listening ports found",
                on_enter=HideWindowAction()
            )]

        if query:
            matched = [p for p in all_ports if query in p["port"] or query.lower() in p["name"].lower()]
            ports = matched if matched else all_ports
            desc_prefix = f"No exact match for '{query}' - showing all" if not matched else f"Matching port {query}"
        else:
            ports = all_ports
            desc_prefix = "Active listening port"

        items = []
        for p in ports[:15]:
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name=f":{p['port']}  {p['name']}  (PID {p['pid']})",
                description=desc_prefix,
                on_enter=ExtensionCustomAction({
                    "module": self.get_keyword(),
                    "pid": p['pid'],
                    "name": p['name'],
                    "port": p['port'],
                    "action": "killport"
                })
            ))

        return items

    def handle_event(self, event_data: dict) -> List[ExtensionResultItem]:
        pid = event_data.get("pid")
        name = event_data.get("name")
        port = event_data.get("port")
        
        try:
            os.kill(pid, signal.SIGTERM)
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name=f"Killed {name} (PID: {pid}) listening on port {port}",
                on_enter=HideWindowAction()
            )]
        except Exception as e:
            logger.error(f"Failed to kill port process {pid}: {e}")
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="Error killing process",
                description=str(e),
                on_enter=HideWindowAction()
            )]

    def get_open_ports(self) -> list:
        """Get all processes listening on ports using lsof."""
        ports = []
        try:
            result = subprocess.run(
                ["lsof", "-i", "-P", "-n"],
                capture_output=True, text=True, timeout=5
            )
            seen = set()
            for line in result.stdout.strip().split("\n")[1:]:
                if "LISTEN" not in line:
                    continue
                parts = line.split()
                if len(parts) < 9:
                    continue
                name = parts[0]
                pid_str = parts[1]
                addr = parts[8]  # e.g. 127.0.0.1:8080 or *:8080
                port = addr.rsplit(":", 1)[-1]
                try:
                    pid = int(pid_str)
                except ValueError:
                    continue
                key = (pid, port)
                if key in seen:
                    continue
                seen.add(key)
                ports.append({"pid": pid, "name": name, "port": port})
            ports.sort(key=lambda x: int(x["port"]) if x["port"].isdigit() else 0)
        except Exception as e:
            logger.error(f"Error getting open ports: {e}")
        return ports
