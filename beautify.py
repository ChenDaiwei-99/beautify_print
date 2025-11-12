# beautify.py
"""
A module for beautifying console output using Rich library.
Provides both decorator and direct function approaches for pretty printing.
"""

from functools import wraps
from typing import Any, Optional, Callable
from rich.console import Console
from rich.pretty import Pretty
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
import builtins
import inspect


class BeautifyPrinter:
    """A customizable pretty printer using Rich library."""
    
    def __init__(self, console: Optional[Console] = None):
        """
        Initialize BeautifyPrinter with a Rich console.
        
        Args:
            console: Optional Rich Console instance. Creates new if None.
        """
        self.console = console or Console()
        self._original_print = builtins.print
    
    def print(self, *args, sep: str = " ", **kwargs):
        """
        Enhanced print function with automatic beautification.
        
        Args:
            *args: Objects to print
            sep: Separator between objects
            **kwargs: Additional Rich console.print kwargs
        """
        # Handle multiple arguments
        if len(args) > 1:
            output = sep.join(str(arg) for arg in args)
            self.console.print(Pretty(output, expand_all=True, indent_guides=True), **kwargs)
        elif len(args) == 1:
            self.console.print(Pretty(args[0], expand_all=True, indent_guides=True), **kwargs)
        else:
            self.console.print(**kwargs)
    
    def print_with_title(self, obj: Any, title: str = "", width: int = 100, **kwargs):
        """
        Print object with a formatted title header.
        
        Args:
            obj: Object to print
            title: Title to display
            width: Width of the separator line
            **kwargs: Additional Rich console.print kwargs
        """
        if title:
            # Create a centered title with separators
            separator = "-" * ((width - len(title) - 2) // 2)
            formatted_title = f"[bold cyan]{separator} {title} {separator}[/bold cyan]"
            self.console.print(formatted_title)
        
        self.console.print(Pretty(obj, expand_all=True, indent_guides=True), **kwargs)
    
    def print_panel(self, obj: Any, title: str = "", **kwargs):
        """
        Print object inside a Rich panel.
        
        Args:
            obj: Object to print
            title: Panel title
            **kwargs: Additional Panel kwargs
        """
        pretty_obj = Pretty(obj, expand_all=True, indent_guides=True)
        panel = Panel(pretty_obj, title=title, **kwargs)
        self.console.print(panel)
    
    def print_markdown(self, text: str, **kwargs):
        """
        Print text as formatted Markdown.
        
        Args:
            text: Markdown text to print
            **kwargs: Additional console.print kwargs
        """
        md = Markdown(text)
        self.console.print(md, **kwargs)
    
    def monkey_patch_print(self):
        """Replace built-in print with beautified version."""
        builtins.print = self.print
    
    def restore_print(self):
        """Restore original built-in print function."""
        builtins.print = self._original_print


# Create a global instance
beautifier = BeautifyPrinter()


# Convenience functions for direct use
def bprint(*args, **kwargs):
    """Direct beautified print function."""
    beautifier.print(*args, **kwargs)


def bprint_title(obj: Any, title: str = "", **kwargs):
    """Print with title header."""
    beautifier.print_with_title(obj, title, **kwargs)


def bprint_panel(obj: Any, title: str = "", **kwargs):
    """Print in a panel."""
    beautifier.print_panel(obj, title, **kwargs)


def bprint_md(text: str, **kwargs):
    """Print as Markdown."""
    beautifier.print_markdown(text, **kwargs)


# Decorator approach
def beautify_output(title: str = "", panel: bool = False):
    """
    Decorator to beautify function return values.
    
    Args:
        title: Optional title to display
        panel: Whether to display in a panel
        
    Returns:
        Decorated function that pretty-prints its return value
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Generate title from function name if not provided
            display_title = title or f"Output from {func.__name__}"
            
            if panel:
                beautifier.print_panel(result, title=display_title)
            else:
                beautifier.print_with_title(result, title=display_title)
            
            return result
        return wrapper
    return decorator


# Context manager for temporary print replacement
class BeautifyContext:
    """Context manager for temporarily replacing print with beautified version."""
    
    def __enter__(self):
        beautifier.monkey_patch_print()
        return beautifier
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        beautifier.restore_print()


# Simplified API
def enable_beautiful_print():
    """Enable beautified printing globally."""
    beautifier.monkey_patch_print()


def disable_beautiful_print():
    """Disable beautified printing globally."""
    beautifier.restore_print()