import json
import mimetypes
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
)

from .db import FileSystemDatabase
from .services import EntityMove

# Get templates from the main app
from .templates import templates
from .utils import (
    Format,
    RequestedFormat,
    get_linux_users,
)

router = APIRouter()


@router.get("/users")
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


@router.get("/users/{username}/{path:path}")
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


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request},
    )


@router.get("/actions/move_entity/")
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
