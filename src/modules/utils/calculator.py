import logging
import math
import re
from typing import List
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)

class CalculatorModule(BaseModule):
    """Evaluate math expressions safely"""

    def get_keyword(self) -> str:
        return "calc"

    def get_icon(self) -> str:
        return "images/icon.svg"

    def handle_query(self, query: str) -> List[ExtensionResultItem]:
        query = query.strip()
        if not query:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="Calculator",
                description="Enter math expression (e.g. 2 + 2, 5% of 100, sqrt(16))",
                on_enter=None
            )]

        # Pre-process for natural language math
        processed_query = query.lower()
        processed_query = processed_query.replace("x", "*")
        processed_query = processed_query.replace("^", "**")
        processed_query = processed_query.replace("% of", "* 0.01 *")
        processed_query = processed_query.replace("percent of", "* 0.01 *")

        try:
            # Basic safety check: only allow numbers, operators, and math functions
            # This is a simple whitelist approach
            allowed_chars = set("0123456789+-*/().**% ")
            if not all(c in allowed_chars for c in processed_query):
                # Check for math functions
                math_funcs = ["sqrt", "sin", "cos", "tan", "log", "exp", "pi", "e"]
                temp_query = processed_query
                for func in math_funcs:
                    temp_query = temp_query.replace(func, "")
                
                if not all(c in allowed_chars for c in temp_query):
                    return [ExtensionResultItem(
                        icon=self.get_icon(),
                        name="Invalid expression",
                        description="Only basic math and common functions are supported.",
                        on_enter=None
                    )]

            # Context for evaluation
            safe_dict = {
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "exp": math.exp,
                "pi": math.pi,
                "e": math.e,
                "__builtins__": None
            }

            result = eval(processed_query, {"__builtins__": None}, safe_dict)
            
            # Format result
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            result_str = str(result)

            return [ExtensionResultItem(
                icon=self.get_icon(),
                name=result_str,
                description="Result of calculation. Press Enter to copy.",
                on_enter=CopyToClipboardAction(result_str)
            )]

        except ZeroDivisionError:
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="Error: Division by zero",
                description="Please check your expression.",
                on_enter=HideWindowAction()
            )]
        except Exception as e:
            logger.debug(f"Calculation failed: {e}")
            return [ExtensionResultItem(
                icon=self.get_icon(),
                name="Result: ...",
                description="Continue typing your expression...",
                on_enter=None
            )]
