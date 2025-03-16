from enum import Enum
from typing import Annotated

from fastapi import Depends, Query, Request


# Define Format enum for better type hinting
class Format(str, Enum):
    HTML = "html"
    JSON = "json"
    MARKDOWN = "md"
    RAW = "raw"
    YAML = "yaml"
    XML = "xml"


# Create a dependency for format determination
def FormatDependency(
    request: Request,
    format: str = Query(
        None, description="Response format (html, json, md, raw, yaml, xml)"
    ),
) -> Format:
    """
    FastAPI dependency that determines the response format based on
    query parameters or Accept headers.
    """
    if format:
        return Format(format.lower())

    accept_header = request.headers.get("accept", "")
    if "application/json" in accept_header:
        return Format.JSON
    elif "text/markdown" in accept_header:
        return Format.MARKDOWN
    elif "application/yaml" in accept_header or "text/yaml" in accept_header:
        return Format.YAML
    elif "application/xml" in accept_header or "text/xml" in accept_header:
        return Format.XML
    elif "text/html" in accept_header:
        return Format.HTML
    return Format.RAW  # Default format changes to RAW


# Create a type alias for the annotated dependency
RequestedFormat = Annotated[Format, Depends(FormatDependency)]


def get_capital_directories():
    """Get all directories in the home folder that start with a capital letter."""
    from pathlib import Path

    home_dir = Path.home()

    # List all items in the home directory
    all_items = [item for item in home_dir.iterdir()]

    # Filter for directories starting with a capital letter
    capital_dirs = [
        {"name": item.name, "path": str(item), "is_dir": item.is_dir()}
        for item in all_items
        if item.is_dir() and item.name[0].isupper()
    ]

    return capital_dirs
