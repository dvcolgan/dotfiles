import mimetypes
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import FileSystemDatabase
from .settings import BASE_DIR

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Create file system database
fs_db = FileSystemDatabase(Path.home())

# Add Path to global template context
templates.env.globals["Path"] = Path

templates.env.filters["datetime"] = (
    lambda timestamp: timestamp
    and datetime.fromtimestamp(timestamp or "").strftime("%Y-%m-%d %H:%M:%S")
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


@app.get("/users", response_class=HTMLResponse)
async def list_linux_users(request: Request):
    """Endpoint to display all Linux users on the system."""
    users = get_linux_users()

    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users,
        },
    )


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request},
    )


@app.get("/{path:path}")
async def file_browser(request: Request, path: str = ""):
    """Browse files and folders at the specified path."""
    # Handle empty path (root)
    if not path:
        path = "/"

    # Create Path object
    file_path = Path(path) if path.startswith("/") else Path(f"/{path}")

    # If it's a directory, show the directory contents
    if file_path.is_dir():
        # Get directory contents using FileSystemDatabase
        items = fs_db.list_directory(file_path)

        # Get breadcrumbs for navigation
        breadcrumbs = fs_db.get_breadcrumbs(file_path)

        return templates.TemplateResponse(
            "folder.html",
            {
                "request": request,
                "path": str(file_path),
                "items": items,
                "breadcrumbs": breadcrumbs,
            },
        )

    # If it's a file, serve the file
    elif file_path.is_file():
        # Get file model from the database
        file_model = fs_db.get(file_path)

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
