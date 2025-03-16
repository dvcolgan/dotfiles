from enum import Enum
from typing import Annotated

from fastapi import Depends, Query, Request


# Define Format enum for better type hinting
class Format(str, Enum):
    HTML = "html"
    JSON = "json"
    MARKDOWN = "md"


# Create a dependency for format determination
def FormatDependency(
    request: Request,
    format: str = Query(None, description="Response format (html, json, md)"),
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
    return Format.HTML  # Default format


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


def get_linux_users():
    """Get all Linux users on the system."""
    users = []
    try:
        import pwd

        for user in pwd.getpwall():
            # Include only real users (typically UID >= 1000)
            if (
                user.pw_uid >= 1000
                and user.pw_shell != "/usr/sbin/nologin"
                and user.pw_shell != "/bin/false"
            ):
                users.append(
                    {
                        "username": user.pw_name,
                        "uid": user.pw_uid,
                        "home_dir": user.pw_dir,
                        "shell": user.pw_shell,
                    }
                )
    except ImportError:
        # Handle case when pwd is not available (e.g., on Windows)
        pass
    return users


# Mock database for demonstration purposes
entity_database = {
    "player": {"x": 0, "y": 0, "type": "player"},
    "enemy_1": {"x": 10, "y": 20, "type": "enemy"},
    "chest": {"x": 15, "y": 30, "type": "item"},
}
