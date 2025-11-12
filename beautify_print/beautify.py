# beautify.py
"""
A module for beautifying console output using Rich library.
Provides a unified bprint function with multiple output modes.
"""

from functools import wraps
from typing import Any, Optional, Callable, Literal, Union
from rich.console import Console
from rich.pretty import Pretty
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax
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
    
    def print(
        self,
        *args,
        # Display options
        title: str = "",
        panel: bool = False,
        markdown: bool = False,
        code: bool = False,
        table: bool = False,
        
        # Formatting options
        sep: str = " ",
        expand_all: bool = True,
        indent_guides: bool = True,
        
        # Panel specific options
        panel_style: str = "bold cyan",
        panel_expand: bool = True,
        
        # Title specific options
        title_width: int = 100,
        title_style: str = "bold cyan",
        title_align: Literal["left", "center", "right"] = "center",
        
        # Code specific options
        language: str = "python",
        theme: str = "monokai",
        line_numbers: bool = False,
        
        # Additional Rich console.print kwargs
        **kwargs
    ):
        """
        Unified beautified print function with multiple display modes.
        
        Args:
            *args: Objects to print
            
            Display Mode Options:
            - title: Add a formatted title header
            - panel: Display in a Rich panel
            - markdown: Render as Markdown (first arg must be string)
            - code: Display as syntax-highlighted code (first arg must be string)
            - table: Display as a table (first arg must be dict, list of dicts, or list of lists)
            
            Formatting Options:
            - sep: Separator between multiple arguments
            - expand_all: Expand all containers in Pretty output
            - indent_guides: Show indent guides in Pretty output
            
            Panel Options:
            - panel_style: Style for the panel border
            - panel_expand: Whether to expand panel to full width
            
            Title Options:
            - title_width: Total width for title separator
            - title_style: Style for the title text
            - title_align: Alignment of title ("left", "center", "right")
            
            Code Options:
            - language: Programming language for syntax highlighting
            - theme: Color theme for syntax highlighting
            - line_numbers: Whether to show line numbers
            
            **kwargs: Additional Rich console.print kwargs
        """
        # Handle empty args
        if not args:
            self.console.print(**kwargs)
            return
        
        # Prepare the content
        if len(args) > 1:
            content = sep.join(str(arg) for arg in args)
        else:
            content = args[0]
        
        # Handle different display modes
        if markdown:
            # Markdown mode
            if not isinstance(content, str):
                content = str(content)
            output = Markdown(content)
        
        elif code:
            # Code/syntax highlighting mode
            if not isinstance(content, str):
                content = str(content)
            output = Syntax(
                content,
                language,
                theme=theme,
                line_numbers=line_numbers
            )
        
        elif table and isinstance(content, (list, dict)):
            # Table mode
            output = self._create_table(content)
        
        else:
            # Pretty print mode (default)
            output = Pretty(
                content,
                expand_all=expand_all,
                indent_guides=indent_guides
            )
        
        # Apply title if specified
        if title and not panel:  # Title without panel
            self._print_with_title(output, title, title_width, title_style, title_align, **kwargs)
        
        # Apply panel if specified
        elif panel:
            panel_kwargs = {
                "title": title if title else None,
                "style": panel_style,
                "expand": panel_expand
            }
            self.console.print(Panel(output, **panel_kwargs), **kwargs)
        
        # Direct output
        else:
            self.console.print(output, **kwargs)
    
    def _print_with_title(
        self, 
        obj: Any, 
        title: str, 
        width: int,
        style: str,
        align: str,
        **kwargs
    ):
        """Internal method to print with formatted title."""
        if align == "center":
            # Centered title with separators
            separator_len = (width - len(title) - 2) // 2
            left_sep = "-" * separator_len
            right_sep = "-" * (width - len(title) - 2 - separator_len)
            formatted_title = f"[{style}]{left_sep} {title} {right_sep}[/{style}]"
        elif align == "left":
            # Left-aligned title
            separator = "-" * (width - len(title) - 1)
            formatted_title = f"[{style}]{title} {separator}[/{style}]"
        else:  # right
            # Right-aligned title
            separator = "-" * (width - len(title) - 1)
            formatted_title = f"[{style}]{separator} {title}[/{style}]"
        
        self.console.print(formatted_title)
        self.console.print(obj, **kwargs)
    
    def _create_table(self, data: Union[dict, list]) -> Table:
        """Create a Rich table from data."""
        table = Table(show_header=True, header_style="bold magenta")
        
        if isinstance(data, dict):
            # Dictionary: keys as columns, values as single row
            for key in data.keys():
                table.add_column(str(key))
            table.add_row(*[str(v) for v in data.values()])
        
        elif isinstance(data, list) and data:
            if isinstance(data[0], dict):
                # List of dictionaries
                keys = data[0].keys()
                for key in keys:
                    table.add_column(str(key))
                for item in data:
                    table.add_row(*[str(item.get(k, "")) for k in keys])
            
            elif isinstance(data[0], (list, tuple)):
                # List of lists/tuples - first item as headers
                headers = data[0]
                for header in headers:
                    table.add_column(str(header))
                for row in data[1:]:
                    table.add_row(*[str(item) for item in row])
            
            else:
                # Simple list - single column
                table.add_column("Value")
                for item in data:
                    table.add_row(str(item))
        
        return table
    
    def monkey_patch_print(self):
        """Replace built-in print with beautified version."""
        builtins.print = lambda *args, **kwargs: self.print(*args, **kwargs)
    
    def restore_print(self):
        """Restore original built-in print function."""
        builtins.print = self._original_print


# Create a global instance
beautifier = BeautifyPrinter()


# Main unified function
def bprint(*args, **kwargs):
    """
    Unified beautified print function.
    
    Examples:
        # Simple pretty print
        bprint(data)
        
        # With title
        bprint(data, title="Results")
        
        # In a panel
        bprint(data, panel=True, title="User Info")
        
        # As markdown
        bprint("# Header\\n- Item", markdown=True)
        
        # As code with syntax highlighting
        bprint(code_string, code=True, language="python")
        
        # As table
        bprint([{"name": "Alice", "age": 30}], table=True)
        
        # Combined options
        bprint(data, title="API Response", panel=True, expand_all=True)
    """
    beautifier.print(*args, **kwargs)


# Decorator approach with new unified function
def beautify_output(
    title: str = "",
    panel: bool = False,
    markdown: bool = False,
    code: bool = False,
    table: bool = False,
    **kwargs
):
    """
    Decorator to beautify function return values.
    
    Args:
        title: Optional title to display
        panel: Whether to display in a panel
        markdown: Render as Markdown
        code: Display as syntax-highlighted code
        table: Display as table
        **kwargs: Additional arguments passed to bprint
        
    Returns:
        Decorated function that pretty-prints its return value
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **func_kwargs):
            result = func(*args, **func_kwargs)
            
            # Generate title from function name if not provided
            display_title = title or f"Output from {func.__name__}"
            
            bprint(
                result,
                title=display_title,
                panel=panel,
                markdown=markdown,
                code=code,
                table=table,
                **kwargs
            )
            
            return result
        return wrapper
    return decorator


# Context manager for temporary print replacement
class BeautifyContext:
    """Context manager for temporarily replacing print with beautified version."""
    
    def __init__(self, **default_kwargs):
        """
        Initialize context with default arguments for all prints.
        
        Args:
            **default_kwargs: Default arguments to apply to all prints in context
        """
        self.default_kwargs = default_kwargs
    
    def __enter__(self):
        self._original_print = builtins.print
        # Create a custom print that includes default kwargs
        builtins.print = lambda *args, **kwargs: bprint(
            *args, 
            **{**self.default_kwargs, **kwargs}
        )
        return beautifier
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        builtins.print = self._original_print


# Convenience functions for common use cases
def enable_beautiful_print(**default_kwargs):
    """
    Enable beautified printing globally.
    
    Args:
        **default_kwargs: Default arguments for all beautified prints
    """
    builtins.print = lambda *args, **kwargs: bprint(*args, **{**default_kwargs, **kwargs})


def disable_beautiful_print():
    """Disable beautified printing globally."""
    beautifier.restore_print()


# Preset functions for common patterns
class BPrint:
    """Namespace for preset beautify print functions."""
    
    @staticmethod
    def debug(obj: Any, name: str = "DEBUG"):
        """Print debug information with automatic variable name detection."""
        bprint(obj, title=f"🐛 {name}", panel=True, panel_style="red")
    
    @staticmethod
    def info(obj: Any, title: str = "INFO"):
        """Print informational message."""
        bprint(obj, title=f"ℹ️  {title}", panel=True, panel_style="blue")
    
    @staticmethod
    def success(obj: Any, title: str = "SUCCESS"):
        """Print success message."""
        bprint(obj, title=f"✅ {title}", panel=True, panel_style="green")
    
    @staticmethod
    def warning(obj: Any, title: str = "WARNING"):
        """Print warning message."""
        bprint(obj, title=f"⚠️  {title}", panel=True, panel_style="yellow")
    
    @staticmethod
    def error(obj: Any, title: str = "ERROR"):
        """Print error message."""
        bprint(obj, title=f"❌ {title}", panel=True, panel_style="red bold")
    
    @staticmethod
    def json(obj: Any, title: str = ""):
        """Print as formatted JSON-like structure."""
        kwargs = {"title": title} if title else {}
        bprint(obj, panel=True, expand_all=True, indent_guides=True, **kwargs)