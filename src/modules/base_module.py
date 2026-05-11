import logging
import os
from abc import ABC, abstractmethod
from typing import List
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

logger = logging.getLogger(__name__)

class BaseModule(ABC):
    """Base class for all OmniPack modules."""

    def __init__(self, extension):
        self.extension = extension

    @abstractmethod
    def get_keyword(self) -> str:
        """Return the sub-keyword for this module."""
        pass

    @abstractmethod
    def get_icon(self) -> str:
        """Return the icon path for this module."""
        pass

    def is_enabled(self) -> bool:
        """Check if the module is enabled in preferences."""
        enabled_group = self.extension.preferences.get("enabled_modules", "all")
        if enabled_group == "all":
            return True
        
        # Determine category based on module path
        # src/modules/dev/uuid_gen.py -> category = dev
        import inspect
        module_file = inspect.getfile(self.__class__)
        category = os.path.basename(os.path.dirname(module_file))
        
        return enabled_group == category

    @abstractmethod
    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        """Handle the user query and return a list of result items."""
        pass

    def handle_event(self, event_data: dict) -> List[ExtensionResultItem]:
        """Handle custom events (e.g., ItemEnterEvent). Default is no-op."""
        return []
