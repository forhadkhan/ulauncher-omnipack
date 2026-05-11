import logging
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)

class GoogleSearchModule(BaseModule):
    """Direct Google search"""

    def get_keyword(self) -> str:
        return "g"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        query = query.strip()
        if not query:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="Google Search",
                description="Enter search query...",
                on_enter=None
            )]

        search_url = f"https://www.google.com/search?q={query}"
        return [ExtensionResultItem(
            icon=self.get_icon(),
            name=f"Search Google for '{query}'",
            description=f"Open {search_url} in your browser",
            on_enter=OpenUrlAction(search_url)
        )]
