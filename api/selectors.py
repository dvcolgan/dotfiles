import mimetypes
from pathlib import Path

import yaml
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    PlainTextResponse,
)

from .db import FileSystemDatabase

# Get templates from the main app
from .templates import templates
from .users import get_linux_users
from .utils import (
    Format,
    RequestedFormat,
)

router = APIRouter()


@router.get("/home")
async def list_users(request: Request, format: RequestedFormat):
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


@router.get("/home/{username}/{path:path}")
async def user_file_browser(
    request: Request,
    format: RequestedFormat,
    username: str,
    path: str = "",
):
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

        # Return appropriate response based on format
        if format == Format.JSON:
            return {
                "path": str(file_path),
                "username": username,
                "items": items,
                "breadcrumbs": breadcrumbs,
            }
        elif format == Format.MARKDOWN:
            return templates.TemplateResponse(
                "folder.md",
                {
                    "request": request,
                    "path": str(file_path),
                    "username": username,
                    "items": items,
                    "breadcrumbs": breadcrumbs,
                },
                media_type="text/markdown",
            )
        elif format == Format.YAML:
            content = yaml.dump(
                {
                    "path": str(file_path),
                    "username": username,
                    "items": items,
                    "breadcrumbs": breadcrumbs,
                }
            )
            return PlainTextResponse(content, media_type="application/yaml")
        else:  # Default to HTML
            return templates.TemplateResponse(
                "folder.html",
                {
                    "request": request,
                    "path": str(file_path),
                    "username": username,
                    "items": items,
                    "breadcrumbs": breadcrumbs,
                },
                media_type="text/html",
            )

    # If it's a file, serve the file
    elif file_path.is_file():
        # Get file model from the database
        file_model = user_fs_db.get(file_path)

        # Determine mime type
        mime_type = (
            file_model.metadata.mime_type or mimetypes.guess_type(str(file_path))[0]
        )

        # For RAW format or binary files, serve directly
        if format == Format.RAW or (
            mime_type
            and (mime_type.startswith("image/") or not mime_type.startswith("text/"))
            and not mime_type.startswith("application/json")
        ):
            return FileResponse(file_path)

        # For other formats, handle based on format
        if format == Format.JSON:
            # Return file metadata and content if possible
            response_data = {
                "path": str(file_path),
                "name": file_path.name,
                "size": file_path.stat().st_size,
                "mime_type": mime_type,
                "metadata": file_model.metadata.dict()
                if hasattr(file_model.metadata, "dict")
                else {},
            }

            # Include content for text files
            if mime_type and (
                mime_type.startswith("text/") or mime_type == "application/json"
            ):
                response_data["content"] = (
                    file_model.content if isinstance(file_model.content, str) else None
                )

            return response_data

        elif format == Format.MARKDOWN:
            template_name = (
                f"file_previews/{file_model.template_name}.md"
                if hasattr(file_model, "template_name")
                else "file_previews/default.md"
            )
            return templates.TemplateResponse(
                template_name,
                {
                    "request": request,
                    "file": file_model,
                    "path": str(file_path),
                    "username": username,
                    "mime_type": mime_type,
                },
                media_type="text/markdown",
            )

        elif format == Format.YAML:
            response_data = {
                "path": str(file_path),
                "name": file_path.name,
                "size": file_path.stat().st_size,
                "mime_type": mime_type,
                "metadata": file_model.metadata.dict()
                if hasattr(file_model.metadata, "dict")
                else {},
            }
            if mime_type and (
                mime_type.startswith("text/") or mime_type == "application/json"
            ):
                response_data["content"] = (
                    file_model.content if isinstance(file_model.content, str) else None
                )
            return PlainTextResponse(
                yaml.dump(response_data), media_type="application/yaml"
            )

        elif format == Format.HTML:
            return templates.TemplateResponse(
                file_model.template_name,
                {
                    "request": request,
                    "file": file_model,
                    "path": str(file_path),
                    "username": username,
                    "mime_type": mime_type,
                },
                media_type="text/html",
            )

        # For text files with no specific format requested, return content as plain text
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
