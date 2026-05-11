import logging
import sys
import os

# Add the project root to sys.path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.core.extension import OmniExtension
from src.modules.dev.uuid_gen import UUIDGenModule
from src.modules.dev.password_gen import PasswordGenModule
from src.modules.system.kill_process import KillProcessModule
from src.modules.system.kill_port import KillPortModule
from src.modules.system.empty_trash import EmptyTrashModule
from src.modules.web.google_search import GoogleSearchModule
from src.modules.web.google_ai import GoogleAIModule
from src.modules.utils.file_search import FileSearchModule
from src.modules.utils.calculator import CalculatorModule

logging.basicConfig()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    extension = OmniExtension()
    
    # Register modules
    extension.register_module(UUIDGenModule)
    extension.register_module(PasswordGenModule)
    extension.register_module(KillProcessModule)
    extension.register_module(KillPortModule)
    extension.register_module(EmptyTrashModule)
    extension.register_module(GoogleSearchModule)
    extension.register_module(GoogleAIModule)
    extension.register_module(FileSearchModule)
    extension.register_module(CalculatorModule)
    
    extension.run()