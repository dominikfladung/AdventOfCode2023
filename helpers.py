"""Utility functions for the project."""

def binary_to_decimal(binary: str) -> int:
    """Converts a binary number to a decimal number."""
    return int(binary, 2)

def import_input(file_name: str) -> str:
    """Reads a file and returns its content."""
    with open(f"./inputs/{str(file_name)}.txt", encoding="utf-8") as f:
        return f.read().splitlines();