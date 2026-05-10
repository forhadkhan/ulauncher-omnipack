"""OmniPack - Ulauncher extension with multiple utilities."""
import logging
import uuid as uuid_lib
import random
import string
import subprocess
import os
import signal
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.event import ItemEnterEvent

logger = logging.getLogger(__name__)


def generate_password(length: int = 16) -> str:
    """Generate a secure random password."""
    chars = string.ascii_letters + string.digits + "!@#$%&*"
    return "".join(random.choice(chars) for _ in range(length))


def get_processes(search: str = "") -> list:
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
                pid = int(parts[0])
                name = parts[1]
                cmd = parts[2] if len(parts) > 2 else name
                if search and search.lower() not in name.lower() and search.lower() not in cmd.lower():
                    continue
                processes.append({"pid": pid, "name": name, "cmd": cmd[:80]})
        processes.sort(key=lambda x: x["name"].lower())
    except Exception as e:
        logger.error(f"Error getting processes: {e}")
    return processes


def get_port_process(port: int) -> dict | None:
    """Get process listening on a specific port."""
    try:
        result = subprocess.run(
            ["ss", "-tlnp", f"sport = :{port}"],
            capture_output=True, text=True, timeout=2
        )
        for line in result.stdout.strip().split("\n")[1:]:
            if not line.strip():
                continue
            # Parse ss output: State Recv-Q Send-Q Local Address:Port Peer Address:Port Process
            parts = line.split()
            if len(parts) >= 6:
                # Extract PID from process column (e.g., "users:(("nginx",pid=1234,fd=6))")
                proc_info = parts[-1]
                if "pid=" in proc_info:
                    pid_str = proc_info.split("pid=")[1].split(",")[0]
                    pid = int(pid_str)
                    name = proc_info.split('"')[1] if '"' in proc_info else "unknown"
                    return {"pid": pid, "name": name, "port": port}
    except Exception as e:
        logger.error(f"Error getting port process: {e}")
    return None


class KeywordQueryEventListener(EventListener):
    """Handle keyword query events."""

    def on_event(self, event, extension):
        """Handle query based on keyword."""
        uuid_kw = extension.preferences.get("uuid_kw", "uuid")
        pass_kw = extension.preferences.get("pass_kw", "pass")
        kill_kw = extension.preferences.get("kill_kw", "kill")
        killport_kw = extension.preferences.get("killport_kw", "killport")
        keyword = event.get_keyword()

        if keyword == kill_kw:
            return self.handle_kill(event)
        elif keyword == killport_kw:
            return self.handle_killport(event)
        elif keyword == pass_kw:
            return self.handle_password(event)
        return self.handle_uuid(event)

    def handle_uuid(self, event):
        """Generate UUID on event."""
        query = event.get_argument() or ""
        items = []

        if not query or query in ["v4", "uuid4"]:
            u = str(uuid_lib.uuid4())
            items.append(ExtensionResultItem(
                icon="images/icon.svg",
                name=f"UUID v4: {u}",
                on_enter=CopyToClipboardAction(u)
            ))

        if query in ["v1", "uuid1"]:
            u = str(uuid_lib.uuid1())
            items.append(ExtensionResultItem(
                icon="images/icon.svg",
                name=f"UUID v1: {u}",
                on_enter=CopyToClipboardAction(u)
            ))

        if query in ["v5", "uuid5"]:
            try:
                name = query.split()[1] if " " in query else "example.com"
                u = str(uuid_lib.uuid5(uuid_lib.NAMESPACE_DNS, name))
                items.append(ExtensionResultItem(
                    icon="images/icon.svg",
                    name=f"UUID v5: {u}",
                    on_enter=CopyToClipboardAction(u)
                ))
            except IndexError:
                pass

        if not items:
            u = str(uuid_lib.uuid4())
            items.append(ExtensionResultItem(
                icon="images/icon.svg",
                name=f"UUID v4: {u}",
                on_enter=CopyToClipboardAction(u)
            ))

        return RenderResultListAction(items)

    def handle_password(self, event):
        """Generate passwords on event."""
        query = event.get_argument() or ""
        try:
            length = int(query.split()[0]) if query.split() else 16
            length = max(8, min(length, 64))
        except ValueError:
            length = 16

        items = []
        for _ in range(3):
            pwd = generate_password(length)
            items.append(ExtensionResultItem(
                icon="images/icon.svg",
                name=pwd,
                on_enter=CopyToClipboardAction(pwd)
            ))

        return RenderResultListAction(items)

    def handle_kill(self, event):
        """List and kill processes."""
        query = event.get_argument() or ""
        processes = get_processes(query)
        items = []

        if not processes:
            items.append(ExtensionResultItem(
                icon="images/icon.svg",
                name="No processes found",
                on_enter=HideWindowAction()
            ))
            return RenderResultListAction(items)

        for proc in processes[:15]:
            items.append(ExtensionResultItem(
                icon="images/icon.svg",
                name=f"Kill {proc['name']} (PID: {proc['pid']})",
                description=proc['cmd'],
                on_enter=ExtensionCustomAction({"pid": proc['pid'], "name": proc['name']})
            ))

        return RenderResultListAction(items)

    def handle_killport(self, event):
        """Kill process listening on a port."""
        query = event.get_argument() or ""
        items = []

        if not query:
            items.append(ExtensionResultItem(
                icon="images/icon.svg",
                name="Enter a port number (e.g., killport 3000)",
                on_enter=HideWindowAction()
            ))
            return RenderResultListAction(items)

        try:
            port = int(query.split()[0])
            proc = get_port_process(port)
            if proc:
                items.append(ExtensionResultItem(
                    icon="images/icon.svg",
                    name=f"Kill {proc['name']} (PID: {proc['pid']}) on port {port}",
                    description=f"Process listening on port {port}",
                    on_enter=ExtensionCustomAction({"pid": proc['pid'], "name": proc['name'], "port": port, "action": "killport"})
                ))
            else:
                items.append(ExtensionResultItem(
                    icon="images/icon.svg",
                    name=f"No process found on port {port}",
                    on_enter=HideWindowAction()
                ))
        except ValueError:
            items.append(ExtensionResultItem(
                icon="images/icon.svg",
                name=f"Invalid port number: {query}",
                on_enter=HideWindowAction()
            ))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    """Handle item enter events."""

    def on_event(self, event, extension):
        """Handle kill process action."""
        data = event.get_data()
        pid = data["pid"]
        name = data["name"]
        action_type = data.get("action", "kill")
        port = data.get("port")

        try:
            os.kill(pid, signal.SIGTERM)
            if action_type == "killport":
                msg = f"Killed {name} (PID: {pid}) on port {port}"
            else:
                msg = f"Killed {name} (PID: {pid})"
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.svg",
                    name=msg,
                    on_enter=HideWindowAction()
                )
            ])
        except ProcessLookupError:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.svg",
                    name=f"Process {name} not found",
                    on_enter=HideWindowAction()
                )
            ])
        except PermissionError:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.svg",
                    name=f"Permission denied to kill {name}",
                    on_enter=HideWindowAction()
                )
            ])


class OmniPackExtension(Extension):
    """Main extension class."""

    def __init__(self):
        """Initialize extension."""
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        logger.info("OmniPack extension initialized")


if __name__ == "__main__":
    OmniPackExtension().run()