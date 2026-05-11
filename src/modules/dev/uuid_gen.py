import logging
import uuid as uuid_lib
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)

class UUIDGenModule(BaseModule):
    """Generate UUIDs (v1, v4, v5)"""

    def get_keyword(self) -> str:
        return "uuid"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        query = query.strip().lower()
        items = []

        if not query or query in ["v4", "uuid4"]:
            u = str(uuid_lib.uuid4())
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name=f"UUID v4: {u}",
                description="Click to copy UUID v4 to clipboard",
                on_enter=CopyToClipboardAction(u)
            ))

        if query in ["v1", "uuid1"]:
            u = str(uuid_lib.uuid1())
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name=f"UUID v1: {u}",
                description="Click to copy UUID v1 to clipboard",
                on_enter=CopyToClipboardAction(u)
            ))

        if query.startswith("v5") or query.startswith("uuid5"):
            try:
                name = query.split(None, 1)[1] if " " in query else "example.com"
                u = str(uuid_lib.uuid5(uuid_lib.NAMESPACE_DNS, name))
                items.append(ExtensionResultItem(
                    icon=self.get_icon(),
                    name=f"UUID v5: {u}",
                    description=f"Click to copy UUID v5 (DNS: {name}) to clipboard",
                    on_enter=CopyToClipboardAction(u)
                ))
            except (IndexError, ValueError):
                pass

        if not items and query:
            # If user typed something unknown, show v4 by default
            u = str(uuid_lib.uuid4())
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name=f"UUID v4: {u}",
                description=f"Unknown version '{query}', showing v4 instead",
                on_enter=CopyToClipboardAction(u)
            ))

        return items
