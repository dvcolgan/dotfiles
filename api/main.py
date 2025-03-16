import json
import mimetypes
from enum import Enum
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi import Path as PathParam
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from .db import FileSystemDatabase
from .settings import BASE_DIR


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

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Add Path to global template context
templates.env.globals["Path"] = Path

templates.env.filters["datetime"] = (
    lambda timestamp: timestamp
    # and datetime.fromtimestamp(timestamp or "").strftime("%Y-%m-%d %H:%M:%S")
)


def get_capital_directories():
    """Get all directories in the home folder that start with a capital letter."""
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


@app.get("/users")
async def list_users(request: Request, format: RequestedFormat):
    """
    Endpoint to display all Linux users on the system.

    Supports multiple response formats:
    - HTML (default): Returns rendered template
    - JSON: Returns raw user data
    - MD: Returns markdown template

    Format can be specified via:
    - Query parameter: ?format=json/html/md
    - Accept header: application/json, text/html, text/markdown
    """
    users = get_linux_users()

    # Return appropriate response based on format
    if format == Format.JSON:
        return users
    elif format == Format.MARKDOWN:
        return templates.TemplateResponse(
            "users.md",
            {
                "request": request,
                "users": users,
            },
            media_type="text/markdown",
        )
    else:  # Default to HTML
        return templates.TemplateResponse(
            "users.html",
            {
                "request": request,
                "users": users,
            },
            media_type="text/html",
        )


@app.get("/users/{username}/{path:path}")
async def user_file_browser(request: Request, username: str, path: str = ""):
    """Browse files and folders in a specific user's home directory."""
    # Build the complete path
    base_path = Path("/home") / username

    # Ensure the user's home directory exists
    if not base_path.exists() or not base_path.is_dir():
        raise HTTPException(
            status_code=404, detail=f"User home directory for {username} not found"
        )

    # Handle empty path (user's home directory root)
    file_path = base_path
    if path:
        file_path = base_path / path

    # Create a file system database for this specific user's home
    user_fs_db = FileSystemDatabase(base_path)

    # If it's a directory, show the directory contents
    if file_path.is_dir():
        # Get directory contents using FileSystemDatabase
        items = user_fs_db.list_directory(file_path)

        # Get breadcrumbs for navigation
        breadcrumbs = user_fs_db.get_breadcrumbs(file_path)

        return templates.TemplateResponse(
            "folder.html",
            {
                "request": request,
                "path": str(file_path),
                "username": username,
                "items": items,
                "breadcrumbs": breadcrumbs,
            },
        )

    # If it's a file, serve the file
    elif file_path.is_file():
        # Get file model from the database
        file_model = user_fs_db.get(file_path)

        # Determine mime type
        mime_type = (
            file_model.metadata.mime_type or mimetypes.guess_type(str(file_path))[0]
        )

        # For binary files and images, serve directly
        if (
            mime_type
            and (mime_type.startswith("image/") or not mime_type.startswith("text/"))
            and not mime_type.startswith("application/json")
        ):
            return FileResponse(file_path)

        # For text files, return content as plain text
        if isinstance(file_model.content, str):
            return PlainTextResponse(file_model.content)

        # Fall back to binary for other types
        return FileResponse(file_path)

    # Path doesn't exist
    else:
        raise HTTPException(status_code=404, detail=f"Path {file_path} not found")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request},
    )


# Mock database for demonstration purposes
entity_database = {
    "player": {"x": 0, "y": 0, "type": "player"},
    "enemy_1": {"x": 10, "y": 20, "type": "enemy"},
    "chest": {"x": 15, "y": 30, "type": "item"},
}


class EntityMove(BaseModel):
    """Request model for moving an entity to a position"""

    entity_name: str = Field(..., description="Unique identifier of the entity to move")
    x: float = Field(..., description="Target X coordinate")
    y: float = Field(..., description="Target Y coordinate")


class EntityResponse(BaseModel):
    """Response model for entity data"""

    entity_name: str
    x: float
    y: float
    type: str
    message: str


@app.post("/actions/move_entity/", response_model=EntityResponse)
async def move_entity(move_data: EntityMove):
    """
    Move a game entity to an absolute position defined by x and y coordinates.

    - **entity_name**: The unique identifier of the entity to move
    - **x**: The target X coordinate
    - **y**: The target Y coordinate

    Returns the updated entity information with confirmation message.
    """
    entity_name = move_data.entity_name

    # Check if entity exists
    if entity_name not in entity_database:
        raise HTTPException(status_code=404, detail=f"Entity '{entity_name}' not found")

    # Update entity position
    entity_database[entity_name]["x"] = move_data.x
    entity_database[entity_name]["y"] = move_data.y

    # Return updated entity data
    return EntityResponse(
        entity_name=entity_name,
        x=move_data.x,
        y=move_data.y,
        type=entity_database[entity_name]["type"],
        message=f"Entity '{entity_name}' has been moved to position ({move_data.x}, {move_data.y})",
    )


@app.get("/actions/move_entity/")
async def get_move_entity_action(request: Request, format: RequestedFormat):
    """
    Get information about the move entity action.

    Supports multiple response formats:
    - HTML: Returns a rendered template with action description
    - JSON: Returns the JSON schema of the action inputs
    - MD: Returns a markdown description of the action
    """
    # Get the model schema for documentation
    schema = EntityMove.model_json_schema()

    # Action description for templates
    action_info = {
        "name": "Move Entity",
        "description": "Move a game entity to an absolute position defined by x and y coordinates.",
        "method": "POST",
        "endpoint": "/actions/move_entity/",
        "parameters": [
            {
                "name": "entity_name",
                "type": "string",
                "description": "Unique identifier of the entity to move",
                "required": True,
            },
            {
                "name": "x",
                "type": "number",
                "description": "Target X coordinate",
                "required": True,
            },
            {
                "name": "y",
                "type": "number",
                "description": "Target Y coordinate",
                "required": True,
            },
        ],
        "example": json.dumps({"entity_name": "player", "x": 100, "y": 200}, indent=2),
    }

    # Return appropriate response based on format
    if format == Format.JSON:
        return JSONResponse(content=schema)
    elif format == Format.MARKDOWN:
        return templates.TemplateResponse(
            "action.md",
            {"request": request, "action": action_info},
            media_type="text/markdown",
        )
    else:  # Default to HTML
        return templates.TemplateResponse(
            "action.html",
            {"request": request, "action": action_info},
        )


# Optionally, add an endpoint to get entity information
@app.get("/entities/{entity_name}", response_model=EntityResponse)
async def get_entity(
    entity_name: str = PathParam(..., description="Unique identifier of the entity"),
):
    """Retrieve information about a specific entity"""
    if entity_name not in entity_database:
        raise HTTPException(status_code=404, detail=f"Entity '{entity_name}' not found")

    entity = entity_database[entity_name]
    return EntityResponse(
        entity_name=entity_name,
        x=entity["x"],
        y=entity["y"],
        type=entity["type"],
        message=f"Entity '{entity_name}' information retrieved",
    )
