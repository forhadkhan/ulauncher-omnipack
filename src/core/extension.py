import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from src.core.events import KeywordQueryEventListener, ItemEnterEventListener

logger = logging.getLogger(__name__)

class OmniExtension(Extension):
    """Main extension class that manages modular features."""

    def __init__(self):
        super().__init__()
        self.modules = {}
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        logger.info("OmniExtension initialized")

    def register_module(self, module_class):
        """Register a new module."""
        module = module_class(self)
        kw = module.get_keyword()
        self.modules[kw] = module
        logger.debug(f"Registered module: {kw}")

    def get_module(self, keyword):
        """Get a registered module by its keyword."""
        return self.modules.get(keyword)
