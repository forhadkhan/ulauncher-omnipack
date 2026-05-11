import logging
import urllib.parse
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)

class YouTubeModule(BaseModule):
    """Search YouTube videos"""

    def get_keyword(self) -> str:
        return "yt"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        query = query.strip()
        if not query:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="YouTube Search",
                description="Search for videos on YouTube",
                on_enter=OpenUrlAction("https://www.youtube.com")
            )]

        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        
        return [ExtensionResultItem(
            icon=self.get_icon(),
            name=f"Search YouTube for '{query}'",
            description="Open YouTube search results in browser",
            on_enter=OpenUrlAction(url)
        )]
