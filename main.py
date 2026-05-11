"""OmniPack - Ulauncher extension with multiple utilities."""
import logging
import uuid as uuid_lib
import random
import string
import subprocess
import os
import signal
import shutil
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
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


def get_open_ports(search: str = "") -> list:
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
            if search and search not in port:
                continue
            ports.append({"pid": pid, "name": name, "port": port})
        ports.sort(key=lambda x: int(x["port"]) if x["port"].isdigit() else 0)
    except Exception as e:
        logger.error(f"Error getting open ports: {e}")
    return ports


class KeywordQueryEventListener(EventListener):
    """Handle keyword query events."""

    def on_event(self, event, extension):
        """Handle query based on keyword."""
        uuid_kw = extension.preferences.get("uuid_kw", "uuid")
        pass_kw = extension.preferences.get("pass_kw", "pass")
        kill_kw = extension.preferences.get("kill_kw", "kill")
        killport_kw = extension.preferences.get("killport_kw", "killport")
        emptytrash_kw = extension.preferences.get("emptytrash_kw", "emptytrash")
        ai_kw = extension.preferences.get("ai_kw", "gai")
        google_kw = extension.preferences.get("google_kw", "g")
        keyword = event.get_keyword()

        if keyword == ai_kw:
            return self.handle_ai_search(event)
        elif keyword == google_kw:
            return self.handle_google_search(event)
        elif keyword == emptytrash_kw:
            return self.handle_emptytrash()
        elif keyword == kill_kw:
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
        if not shutil.which("lsof"):
            return RenderResultListAction([ExtensionResultItem(
                icon="images/icon.svg",
                name="lsof not found",
                description="Install lsof to use killport",
                on_enter=HideWindowAction()
            )])

        query = (event.get_argument() or "").strip()
        all_ports = get_open_ports("")

        if not all_ports:
            return RenderResultListAction([ExtensionResultItem(
                icon="images/icon.svg",
                name="No ports are currently listening",
                on_enter=HideWindowAction()
            )])

        if query:
            matched = [p for p in all_ports if query in p["port"]]
            ports = matched if matched else all_ports
            desc_prefix = f"Port {query} not found — showing all" if not matched else f"Matching port {query}"
        else:
            ports = all_ports
            desc_prefix = "Active listening port"

        items = []
        for p in ports[:15]:
            items.append(ExtensionResultItem(
                icon="images/icon.svg",
                name=f":{p['port']}  {p['name']}  (PID {p['pid']})",
                description=desc_prefix,
                on_enter=ExtensionCustomAction({"pid": p['pid'], "name": p['name'], "port": p['port'], "action": "killport"})
            ))

        return RenderResultListAction(items)

    def handle_emptytrash(self):
        """Empty the user trash directly without confirmation."""
        trash_path = os.path.expanduser("~/.local/share/Trash")
        emptied = False
        for subdir in ["files", "info"]:
            path = os.path.join(trash_path, subdir)
            if os.path.exists(path):
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    try:
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            os.unlink(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        emptied = True
                    except Exception as e:
                        logger.error(f"Error removing {item_path}: {e}")

        if emptied:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.svg",
                    name="Trash emptied successfully",
                    on_enter=HideWindowAction()
                )
            ])
        return RenderResultListAction([
            ExtensionResultItem(
                icon="images/icon.svg",
                name="Trash is already empty",
                on_enter=HideWindowAction()
            )
        ])

    def handle_ai_search(self, event):
        """Search in Google AI Mode."""
        query = event.get_argument() or ""
        ai_kw = "gai"
        if query.startswith(ai_kw + " "):
            query = query[len(ai_kw) + 1:]
        if not query:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.svg",
                    name="Google AI Search",
                    description="Enter your search term...",
                    on_enter=None
                )
            ])
        search_url = f"https://www.google.com/search?udm=50&q={query}"
        return RenderResultListAction([
            ExtensionResultItem(
                icon="images/icon.svg",
                name=f"Search for '{query}'",
                description="Open Google AI search results in your browser",
                on_enter=OpenUrlAction(search_url)
            )
        ])

    def handle_google_search(self, event):
        """Search in Google."""
        query = event.get_argument() or ""
        google_kw = "g"
        if query.startswith(google_kw + " "):
            query = query[len(google_kw) + 1:]
        if not query:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.svg",
                    name="Google Search",
                    description="Enter your search term...",
                    on_enter=None
                )
            ])
        search_url = f"https://www.google.com/search?q={query}"
        return RenderResultListAction([
            ExtensionResultItem(
                icon="images/icon.svg",
                name=f"Search for '{query}'",
                description="Open Google search results in your browser",
                on_enter=OpenUrlAction(search_url)
            )
        ])


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