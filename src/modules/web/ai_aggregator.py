import logging
import urllib.parse
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)

class AIAggregatorModule(BaseModule):
    """
    [F13] AI Aggregator
    Keyword: ai
    Links to various AI services like Perplexity, Gemini, ChatGPT, Claude, and Copilot.
    """

    def get_keyword(self) -> str:
        return "ai"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        query = query.strip()
        encoded_query = urllib.parse.quote(query)
        
        services = [
            {
                "name": "Perplexity",
                "description": "Search with Perplexity AI",
                "url": f"https://www.perplexity.ai/search?q={encoded_query}" if query else "https://www.perplexity.ai/",
                "icon": "images/icon.svg"
            },
            {
                "name": "Google AI Mode",
                "description": "Google Search with AI results (udm=50)",
                "url": f"https://www.google.com/search?udm=50&q={encoded_query}" if query else "https://www.google.com/search?udm=50",
                "icon": "images/icon.svg"
            },
            {
                "name": "ChatGPT",
                "description": "Chat with OpenAI ChatGPT",
                "url": f"https://chatgpt.com/?q={encoded_query}" if query else "https://chatgpt.com/",
                "icon": "images/icon.svg"
            },
            {
                "name": "Claude",
                "description": "Chat with Anthropic Claude",
                "url": f"https://claude.ai/new?q={encoded_query}" if query else "https://claude.ai/new",
                "icon": "images/icon.svg"
            },
            {
                "name": "Mistral",
                "description": "Chat with Mistral AI (Le Chat)",
                "url": f"https://chat.mistral.ai/chat/?q={encoded_query}" if query else "https://chat.mistral.ai/",
                "icon": "images/icon.svg"
            }
        ]

        items = []
        for svc in services:
            items.append(ExtensionResultItem(
                icon=svc["icon"],
                name=svc["name"],
                description=f"{svc['description']} {'for \"' + query + '\"' if query else ''}",
                on_enter=OpenUrlAction(svc["url"])
            ))

        return items
