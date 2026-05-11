import logging
import os
import shutil
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)

class EmptyTrashModule(BaseModule):
    """Empty the system trash"""

    def get_keyword(self) -> str:
        return "trash"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        # Always show confirmation first (as per AGENTS.md Notes: "Confirm before delete")
        # Current main.py doesn't confirm, but AGENTS.md says it should.
        
        return [ExtensionResultItem(
            icon=self.get_icon(),
            name="Empty Trash",
            description="Clear all items from trash? This cannot be undone.",
            on_enter=ExtensionCustomAction({
                "module": self.get_keyword(),
                "action": "empty_trash_confirmed"
            })
        )]

    def handle_event(self, event_data: dict) -> List[ExtensionResultItem]:
        action = event_data.get("action")
        if action != "empty_trash_confirmed":
            return []

        trash_path = os.path.expanduser("~/.local/share/Trash")
        emptied = False
        errors = []
        
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
                        errors.append(str(e))

        if errors:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="Completed with errors",
                description=f"Some items couldn't be removed: {', '.join(errors[:2])}",
                on_enter=HideWindowAction()
            )]
        
        if emptied:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="Trash emptied successfully",
                on_enter=HideWindowAction()
            )]
            
        return [ExtensionResultItem(
            icon=self.get_icon(),
            name="Trash is already empty",
            on_enter=HideWindowAction()
        )]
