import logging
import os
import subprocess
import shutil
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.OpenAction import OpenAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)

class FileSearchModule(BaseModule):
    """Search files recursively using glob/grep patterns"""

    def get_keyword(self) -> str:
        return "file" # primary sub-keyword for omni

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        query = query.strip()
        if not query:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="File Search",
                description="Enter filename pattern (e.g. *.py) or path + pattern",
                on_enter=None
            )]

        # Check if query starts with a path
        search_path = self.extension.preferences.get("file_search_path", "~")
        search_path = os.path.expanduser(search_path)
        pattern = query

        if " " in query:
            # Try to split path and pattern if the first part is an existing dir
            parts = query.split(None, 1)
            maybe_path = os.path.expanduser(parts[0])
            if os.path.isdir(maybe_path):
                search_path = maybe_path
                pattern = parts[1]

        items = []
        try:
            # Use 'find' command for performance
            # -maxdepth 3 to avoid hanging on massive systems, can be adjusted
            # Searching for both files and directories
            cmd = ["find", search_path, "-maxdepth", "3", "-iname", f"*{pattern}*"]
            
            # If pattern looks like a glob, use it directly
            if any(char in pattern for char in ["*", "?", "["]):
                cmd = ["find", search_path, "-maxdepth", "3", "-path", f"*/{pattern}"]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            files = result.stdout.strip().split("\n")
            
            # Filter empty results
            files = [f for f in files if f.strip()]

            if not files:
                return [ExtensionResultItem(
                    icon=self.get_icon(),
                    name="No files found",
                    description=f"Could not find matching files in {search_path}",
                    on_enter=HideWindowAction()
                )]

            for f in files[:15]:
                name = os.path.basename(f)
                items.append(ExtensionResultItem(
                    icon=self.get_icon(),
                    name=name,
                    description=f,
                    on_enter=OpenAction(f)
                ))

        except subprocess.TimeoutExpired:
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name="Search timed out",
                description="Try a more specific path or pattern",
                on_enter=HideWindowAction()
            ))
        except Exception as e:
            logger.error(f"File search failed: {e}")
            items.append(ExtensionResultItem(
                icon=self.get_icon(),
                name="Error during search",
                description=str(e),
                on_enter=HideWindowAction()
            ))

        return items
