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
                description="Enter math expression (e.g. 2+2, 5% of 100, 100*5%)",
                on_enter=None
            )]

        # Pre-process for natural language math
        processed_query = query.lower()
        processed_query = processed_query.replace("x", "*")
        processed_query = processed_query.replace("^", "**")
        
        # Handle "percent of" / "% of"
        processed_query = processed_query.replace("% of", "* 0.01 *")
        processed_query = processed_query.replace("percent of", "* 0.01 *")
        
        # Handle "%" suffix (e.g., 5% -> 5*0.01)
        # We use a regex to ensure we don't break things like "% of" already replaced
        processed_query = re.sub(r"(\d+)%", r"(\1 * 0.01)", processed_query)

        try:
            # Basic safety check: only allow numbers, operators, and math functions
            # Whitelist approach for characters
            allowed_chars = set("0123456789+-*/().**% ")
            
            # Check for math functions and constants
            math_funcs = ["sqrt", "sin", "cos", "tan", "log", "exp", "pi", "e", "abs", "round", "pow"]
            
            # Remove allowed words to check for malicious input
            test_query = processed_query
            for func in math_funcs:
                test_query = test_query.replace(func, "")
            
            if not all(c in allowed_chars for c in test_query):
                logger.debug(f"Calculator: Blocked potentially unsafe query: {processed_query}")
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
                "abs": abs,
                "round": round,
                "pow": pow,
                "__builtins__": None
            }

            # Evaluate the expression
            result = eval(processed_query, {"__builtins__": None}, safe_dict)
            
            # Handle list/tuple results from some functions if any
            if isinstance(result, (list, tuple)):
                result_str = str(result)
            elif isinstance(result, (int, float)):
                # Format result
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                
                if isinstance(result, float):
                    result_str = f"{result:.4f}".rstrip('0').rstrip('.')
                else:
                    result_str = str(result)
            else:
                result_str = str(result)

            return [ExtensionResultItem(
                icon=self.get_icon(),
                name=result_str,
                description=f"Result of '{query}'. Press Enter to copy.",
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
            # If it doesn't look like a complete math expression yet, show a placeholder
            # But only if it has some numbers/operators
            if any(c.isdigit() for c in query):
                return [ExtensionResultItem(
                    icon=self.get_icon(),
                    name="...",
                    description="Continue typing your expression...",
                    on_enter=None
                )]
            return []
