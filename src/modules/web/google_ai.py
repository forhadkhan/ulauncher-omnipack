import logging
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)

class GoogleAIModule(BaseModule):
    """Google search with AI results (udm=50)"""

    def get_keyword(self) -> str:
        return "ai"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        query = query.strip()
        if not query:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="Google AI Search",
                description="Enter query for AI-focused search...",
                on_enter=None
            )]

        search_url = f"https://www.google.com/search?udm=50&q={query}"
        return [ExtensionResultItem(
            icon=self.get_icon(),
            name=f"AI Search for '{query}'",
            description=f"Open Google with AI results in your browser",
            on_enter=OpenUrlAction(search_url)
        )]
