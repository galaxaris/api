"""
This module provides utility functions for console output, for debugging colorfully!
"""

import sys
import os
try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
except ImportError:
    print("\n== WARNING: Rich module not found. In order to have colored console output, please install rich with 'pip install rich'. ==")



def __print_message(msg, title, color):
    """
    Private function to print a message with a specific title and color. 
    
    Allows to skip error printing if rich is not installed, without breaking the code.

    :param msg: The message to print
    :param title: The title of the message (e.g., "INFO", "WARNING", "ERROR", "SUCCESS")
    :param color: The color to use for the message (e.g., "blue", "yellow", "red", "green")
    """
    try:
        console.print(Panel(msg, title=f"[bold]{title}[/bold]", border_style=color, width=60))
    except NameError:
        print(f"[{title}] {msg}")

def print_info(msg):
    """
    Prints an informational message to the console in blue color.
    """
    __print_message(msg, "INFO", "blue")

def print_success(msg):
    """
    Prints a success message to the console in green color.
    """
    __print_message(msg, "SUCCESS", "green")

def print_warning(msg):
    """
    Prints a warning message to the console in yellow color.
    """
    __print_message(msg, "WARNING", "yellow")

def print_error(msg):
    """
    Prints an error message to the console in red color.
    """
    __print_message(msg, "ERROR", "red")

print("\n") #Adds an empty line

if __name__ == "__main__":
    print_info("This is an informational message.")
    print_warning("This is a warning message.")
    print_error("This is an error message.")
    print_success("This is a success message.")

    print_info("This is a very long informational message that should be wrapped inside the panel to demonstrate the width setting of the console output.\n It should be displayed in blue color and properly formatted within the panel.\nHmm, let's see how it handles multiple lines and if the formatting remains consistent across different message lengths.")