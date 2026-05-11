import logging
import re
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction

logger = logging.getLogger(__name__)

class KeywordQueryEventListener(EventListener):
    """Handles KeywordQueryEvent and routes it to the appropriate module."""

    def on_event(self, event, extension):
        query = event.get_argument() or ""
        keyword = event.get_keyword()
        
        omni_kw = extension.preferences.get("omni_kw", "omni")
        
        # 1. Handle main 'omni' keyword
        if keyword == omni_kw:
            if not query:
                return self.show_help(extension)
            
            # Check if it's a specific module command (e.g., 'omni uuid')
            parts = query.split(None, 1)
            module_kw = parts[0]
            module_args = parts[1] if len(parts) > 1 else ""
            
            module = extension.get_module(module_kw)
            if module and module.is_enabled():
                return RenderResultListAction(module.handle_query(module_args))
            
            # Smart Resolver: If it looks like math, show calculator result even without 'calc'
            if self.is_likely_math(query):
                calc_module = extension.get_module("calc")
                if calc_module and calc_module.is_enabled():
                    calc_results = calc_module.handle_query(query)
                    if calc_results and "..." not in calc_results[0].get_name():
                        return RenderResultListAction(calc_results)

            # If no specific module, show help or generic results
            return self.show_help(extension, f"Unknown module: {module_kw}" if query else None)

        # 2. Handle direct keyword commands (e.g., 'uuid', 'pass', '=')
        for module in extension.modules.values():
            module_kw = module.get_keyword()
            pref_map = {
                "port": "killport_kw",
                "ai": "ai_kw",
                "g": "google_kw",
                "trash": "emptytrash_kw",
                "file": "file_search_kw",
                "calc": "calc_kw",
                "=": "calc_alias_kw",
                "yt": "youtube_kw"
            }
            pref_id = pref_map.get(module_kw, f"{module_kw}_kw")
            pref_val = extension.preferences.get(pref_id)
            
            # Handle exact match or alias match (especially for '=')
            if pref_val == keyword or (pref_val == "=" and keyword == "="):
                if module.is_enabled():
                    return RenderResultListAction(module.handle_query(query))
                else:
                    return RenderResultListAction([ExtensionResultItem(
                        icon=module.get_icon(),
                        name=f"Module '{module_kw}' is disabled",
                        description="Enable it in extension preferences",
                        on_enter=HideWindowAction()
                    )])

        return self.show_help(extension)

    def is_likely_math(self, query: str) -> bool:
        """Check if query looks like a math expression."""
        if not query:
            return False
        # Starts with number or contains math operators
        return bool(re.match(r'^[0-9\(]', query)) and any(c in "+-*/^%" for c in query)

    def show_help(self, extension, error_msg=None):
        """List all available commands and their descriptions."""
        items = []
        if error_msg:
            items.append(ExtensionResultItem(
                icon="images/icon.svg",
                name=error_msg,
                description="Check the list of available commands below",
                on_enter=HideWindowAction()
            ))
        
        omni_kw = extension.preferences.get("omni_kw", "omni")
        
        # Sort modules by keyword for consistency
        sorted_modules = sorted(extension.modules.items())
        
        for kw, module in sorted_modules:
            if module.is_enabled():
                items.append(ExtensionResultItem(
                    icon=module.get_icon(),
                    name=f"{omni_kw} {kw}",
                    description=module.__doc__ or f"Run {kw} module",
                    # When selected, auto-fill the query to help the user
                    on_enter=SetUserQueryAction(f"{omni_kw} {kw} ")
                ))
        
        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):
    """Handles ItemEnterEvent and routes it to the module that created the item."""

    def on_event(self, event, extension):
        data = event.get_data()
        if not data or "module" not in data:
            logger.warning("Received ItemEnterEvent without module context")
            return HideWindowAction()
        
        module_kw = data["module"]
        module = extension.get_module(module_kw)
        if module:
            return RenderResultListAction(module.handle_event(data))
        
        return HideWindowAction()
