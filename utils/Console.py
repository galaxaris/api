"""
This module provides utility functions for console output, for debugging colorfully!
"""

import sys
import os
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("== WARNING: Colorama module not found. In order to have colored console output, please install colorama with 'pip install colorama'. ==")
    # Define dummy Fore and Style classes to avoid errors
    class Fore:
        RED = ''
        GREEN = ''
        YELLOW = ''
        BLUE = ''
        MAGENTA = ''
        CYAN = ''
        WHITE = ''

    class Style:
        RESET_ALL = ''

def print_message(message, color=Fore.WHITE):
    """
    Prints a message to the console with the specified color.

    :param message: The message to be printed
    :param color: The color to print the message in (default is white)
    """
    print(f"{color}{message}{Style.RESET_ALL}")

def print_info(message):
    """
    Prints an informational message to the console in cyan.

    :param message: The informational message to be printed
    """
    print_message(f"**INFO**: {message}", color=Fore.CYAN)

def print_warning(message):
    """
    Prints a warning message to the console in yellow.

    :param message: The warning message to be printed
    """
    print_message(f"== WARNING: {message} ==", color=Fore.YELLOW)

def print_error(message):
    """
    Prints an error message to the console in red.

    :param message: The error message to be printed
    """
    print_message(f"== ERROR: {message} ==", color=Fore.RED)

print("\n") #Adds an empty line

if __name__ == "__main__":
    print_info("This is an informational message.")
    print_warning("This is a warning message.")
    print_error("This is an error message.")