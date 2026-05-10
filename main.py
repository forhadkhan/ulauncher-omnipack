"""OmniPack - Ulauncher extension with multiple utilities."""
import logging
import uuid as uuid_lib
import random
import string
import subprocess
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
        # Use ps for fast process listing
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
                # Filter by search
                if search and search.lower() not in name.lower() and search.lower() not in cmd.lower():
                    continue
                processes.append({"pid": pid, "name": name, "cmd": cmd[:80]})
        # Sort alphabetically by name
        processes.sort(key=lambda x: x["name"].lower())
    except Exception as e:
        logger.error(f"Error getting processes: {e}")
    return processes


class KeywordQueryEventListener(EventListener):
    """Handle keyword query events."""

    def on_event(self, event, extension):
        """Handle query based on keyword."""
        uuid_kw = extension.preferences.get("uuid_kw", "uuid")
        pass_kw = extension.preferences.get("pass_kw", "pass")
        kill_kw = extension.preferences.get("kill_kw", "kill")
        keyword = event.get_keyword()

        if keyword == kill_kw:
            return self.handle_kill(event)
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


class ItemEnterEventListener(EventListener):
    """Handle item enter events."""

    def on_event(self, event, extension):
        """Handle kill process action."""
        data = event.get_data()
        pid = data["pid"]
        name = data["name"]
        import os
        import signal
        try:
            os.kill(pid, signal.SIGTERM)
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.svg",
                    name=f"Killed {name} (PID: {pid})",
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