import logging
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
            parts = query.split(None, 1)
            
            # If no argument, show all available commands
            if not parts:
                return self.show_help(extension)
            
            # Route to specific module if it exists
            module_kw = parts[0]
            module_args = parts[1] if len(parts) > 1 else ""
            
            module = extension.get_module(module_kw)
            if module and module.is_enabled():
                return RenderResultListAction(module.handle_query(module_args))
            else:
                # If module not found, show help with an error message
                return self.show_help(extension, f"Unknown or disabled module: {module_kw}")

        # 2. Handle direct keyword commands (e.g., 'uuid', 'pass')
        for module in extension.modules.values():
            module_kw = module.get_keyword()
            # Mapping preference IDs: uuid -> uuid_kw, pass -> pass_kw, etc.
            # Special cases: port -> killport_kw, ai -> ai_kw, g -> google_kw, trash -> emptytrash_kw
            pref_map = {
                "port": "killport_kw",
                "ai": "ai_kw",
                "g": "google_kw",
                "trash": "emptytrash_kw",
                "file": "file_search_kw",
                "calc": "calc_kw",
                "=": "calc_alias_kw"
            }
            pref_id = pref_map.get(module_kw, f"{module_kw}_kw")
            
            if extension.preferences.get(pref_id) == keyword:
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
