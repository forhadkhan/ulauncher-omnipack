import logging
import random
import string
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)

class PasswordGenModule(BaseModule):
    """Generate secure random passwords"""

    def get_keyword(self) -> str:
        return "pass"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        try:
            length = int(query.strip()) if query.strip() else 16
            length = max(8, min(length, 64))
        except ValueError:
            length = 16

        items = []
        for _ in range(5): # Show 5 options
            pwd = self.generate_password(length)
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name=pwd,
                description=f"Length: {length}. Click to copy to clipboard",
                on_enter=CopyToClipboardAction(pwd)
            ))

        return items

    def generate_password(self, length: int) -> str:
        """Generate a secure random password."""
        chars = string.ascii_letters + string.digits + "!@#$%&*"
        return "".join(random.choice(chars) for _ in range(length))
