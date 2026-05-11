import logging
import subprocess
import os
import signal
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)

class KillProcessModule(BaseModule):
    """List and kill running processes"""

    def get_keyword(self) -> str:
        return "kill"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        query = query.strip()
        processes = self.get_processes(query)
        items = []

        if not processes:
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name="No processes found",
                description=f"No results matching '{query}'" if query else "Enter process name",
                on_enter=HideWindowAction()
            ))
            return items

        for proc in processes[:15]:
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name=f"Kill {proc['name']} (PID: {proc['pid']})",
                description=proc['cmd'],
                on_enter=ExtensionCustomAction({
                    "module": self.get_keyword(),
                    "pid": proc['pid'],
                    "name": proc['name'],
                    "action": "kill"
                })
            ))

        return items

    def handle_event(self, event_data: dict) -> List[ExtensionResultItem]:
        pid = event_data.get("pid")
        name = event_data.get("name")
        
        try:
            os.kill(pid, signal.SIGTERM)
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name=f"Successfully killed {name} (PID: {pid})",
                on_enter=HideWindowAction()
            )]
        except ProcessLookupError:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name=f"Process {name} not found",
                on_enter=HideWindowAction()
            )]
        except PermissionError:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name=f"Permission denied to kill {name}",
                description="Try running uLauncher with higher privileges (not recommended)",
                on_enter=HideWindowAction()
            )]
        except Exception as e:
            logger.error(f"Failed to kill process {pid}: {e}")
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="Error killing process",
                description=str(e),
                on_enter=HideWindowAction()
            )]

    def get_processes(self, search: str = "") -> list:
        """Get list of processes matching search using ps command."""
        processes = []
        try:
            result = subprocess.run(
                ["ps", "-eo", "pid,comm,args", "--no-headers"],
                capture_output=True, text=True, timeout=2
            )
            for line in result.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                parts = line.split(None, 2)
                if len(parts) >= 2:
                    try:
                        pid = int(parts[0])
                    except ValueError:
                        continue
                    name = parts[1]
                    cmd = parts[2] if len(parts) > 2 else name
                    if search and search.lower() not in name.lower() and search.lower() not in cmd.lower():
                        continue
                    processes.append({"pid": pid, "name": name, "cmd": cmd[:80]})
            processes.sort(key=lambda x: x["name"].lower())
        except Exception as e:
            logger.error(f"Error getting processes: {e}")
        return processes
