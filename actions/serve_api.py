#!/usr/bin/env python

"""
ctx:
    tags: python, fastapi
    folders: ~/repos/dotfiles/actions/





A simple file browser server implemented using FastAPI.

This script creates a web server that allows browsing the filesystem starting from
the user's home directory. It maps file paths relative to the home folder to URLs.
When navigating to a URL:
- If it points to a file, the file content is rendered or downloaded
- If it points to a directory, its contents are listed as clickable links
- If it points to an image file, the image is displayed in the browser
- If it points to a text file (txt, md, card, html, json, yaml), the content is displayed

When viewing a directory, if there's a file in the parent directory with the same name 
as the directory plus a file extension (e.g., "folder.card" for a directory named "folder"),
the contents of that file will be displayed at the top of the directory listing.

The server handles path traversal protection and proper MIME type detection for files.
The design uses a single unified template that can display both directories and
individual items. When viewing a directory, files (including images and text files) 
are previewed inline within the page with their full content visible.
"""

import os
import mimetypes
from pathlib import Path
from typing import Annotated, List, Optional

from fastapi import FastAPI, HTTPException, Request, Query, Form
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="File Browser")

# Create a templates directory for the HTML templates
templates_dir = Path.home() / "templates"
templates_dir.mkdir(exist_ok=True)

# Create a unified template file
template_file = templates_dir / "unified.html"
with open(template_file, "w") as f:
    f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>File Browser - {{ current_path }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        h1 { margin-bottom: 20px; }
        .breadcrumb { margin-bottom: 20px; padding: 10px; background-color: #f8f9fa; }
        .item { display: flex; padding: 5px; border-bottom: 1px solid #eee; align-items: flex-start; }
        .item:hover { background-color: #f8f9fa; }
        .item-name { flex-grow: 1; }
        .item-size { width: 100px; text-align: right; color: #6c757d; }
        .item-date { width: 200px; text-align: right; color: #6c757d; }
        .folder { color: #007bff; }
        .file { color: #212529; }
        .parent { margin-bottom: 10px; }
        .image-container { 
            margin: 20px auto;
            padding: 10px;
            border: 1px solid #ddd;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: inline-block;
        }
        .single-view { text-align: center; }
        img.preview { max-width: 300px; max-height: 200px; margin: 10px 0; }
        img.full { max-width: 100%; max-height: 80vh; }
        .image-info { margin-top: 10px; color: #6c757d; }
        .back-button { margin-top: 20px; }
        .back-button a { 
            padding: 10px 20px; 
            background-color: #007bff; 
            color: white; 
            text-decoration: none;
            border-radius: 4px;
        }
        .back-button a:hover { background-color: #0056b3; }
        .content-preview-container {
            width: 100%;
            margin: 10px 0;
            padding: 0;
            flex-shrink: 0;
            display: block;
        }
        .text-preview-container {
            width: 100%;
            height: auto;
            text-align: left;
            margin-top: 5px;
            margin-bottom: 15px;
            overflow: auto;
            border: 1px solid #ddd;
            padding: 10px;
            font-family: monospace;
            font-size: 12px;
            background-color: #f8f9fa;
            max-height: 400px;
        }
        .text-preview {
            width: 100%;
            overflow: auto;
            white-space: pre-wrap;
        }
        .file-content {
            margin: 20px auto;
            padding: 15px;
            border: 1px solid #ddd;
            background-color: #f8f9fa;
            overflow: auto;
            max-width: 90%;
            max-height: 80vh;
            white-space: pre-wrap;
            font-family: monospace;
        }
        .file-link {
            font-weight: bold;
            margin-bottom: 5px;
            display: block;
        }
        .item-header {
            width: 100%;
            padding: 5px;
            background-color: #e9ecef;
            margin-bottom: 5px;
            border-radius: 3px;
        }
        .folder-description {
            margin: 15px 0;
            padding: 15px;
            background-color: #f0f8ff;
            border-left: 5px solid #007bff;
            border-radius: 3px;
        }
        .folder-description-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #007bff;
        }
    </style>
</head>
<body>
    <h1>File Browser</h1>
    <div class="breadcrumb">
        <a href="/">Home</a> / 
        {% for part in breadcrumbs %}
            <a href="{{ part.path }}">{{ part.name }}</a> / 
        {% endfor %}
    </div>
    
    {% if is_directory %}
        {% if folder_description %}
        <div class="folder-description">
            <div class="folder-description-title">{{ folder_description_filename }}</div>
            {% if folder_description_is_image %}
                <img src="/raw{{ folder_description_path }}" class="preview" alt="{{ folder_description_filename }}">
            {% else %}
                <div class="text-preview">{{ folder_description }}</div>
            {% endif %}
        </div>
        {% endif %}

        {% if current_path != "/" %}
        <div class="parent">
            <a href="{{ parent_path }}">..</a> (Parent Directory)
        </div>
        {% endif %}
        
        {% for item in items %}
            <div class="item">
                <div class="item-header">
                    <div class="file-link">
                        <a href="{{ item.path }}" class="{{ 'folder' if item.is_dir else 'file' }}">
                            {{ item.name }}{{ '/' if item.is_dir else '' }}
                        </a>
                        <span class="item-size">{{ item.size }}</span>
                        <span class="item-date">{{ item.modified }}</span>
                    </div>
                </div>
            </div>
            
            {% if not item.is_dir %}
                <div class="content-preview-container">
                    {% if item.is_image %}
                        <div class="text-preview-container" style="text-align: center;">
                            <img src="/raw{{ item.path }}" class="preview" alt="{{ item.name }}">
                        </div>
                    {% elif item.is_text %}
                        <div class="text-preview-container">
                            <div class="text-preview">{{ item.full_content }}</div>
                        </div>
                    {% else %}
                        <div class="text-preview-container">
                            <p>This file type cannot be previewed. <a href="/raw{{ item.path }}" download>Download</a></p>
                        </div>
                    {% endif %}
                </div>
            {% endif %}
        {% endfor %}
    {% else %}
        <div class="single-view">
            {% if is_image %}
                <div class="image-container">
                    <img src="/raw{{ current_path }}" class="full" alt="{{ file_name }}">
                    <div class="image-info">
                        <p>{{ file_name }} ({{ file_size }})</p>
                    </div>
                </div>
            {% elif is_text %}
                <div class="file-content">{{ file_content }}</div>
            {% else %}
                <p>This file type cannot be previewed. <a href="/raw{{ current_path }}" download>Download</a></p>
            {% endif %}
            
            <div class="back-button">
                <a href="{{ parent_path }}">Back to Directory</a>
            </div>
        </div>
    {% endif %}
</body>
</html>
    """)

templates = Jinja2Templates(directory=str(templates_dir))

# Get the user's home directory
HOME_DIR = Path.home()

# List of image file extensions
IMAGE_EXTENSIONS = [
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', 
    '.tiff', '.tif', '.svg', '.ico', '.heic', '.heif'
]

# List of text file extensions that should be displayed with preview
TEXT_FILE_EXTENSIONS = [
    '.txt', '.md', '.markdown', '.card', '.html', '.htm', '.toml',
    '.json', '.yaml', '.yml', '.py', '.js', '.css', '.xml',
    '.csv', '.log', '.sh', '.bat', '.rst', '.conf', '.ini'
]

# List of text file MIME types
TEXT_MIME_TYPES = [
    "text/", "application/json", "application/xml", 
    "application/javascript", "application/x-javascript"
]


def is_safe_path(path: Path) -> bool:
    """Check if the path is safe and doesn't try to access files outside HOME_DIR."""
    try:
        # Resolve to absolute path and check if it's within HOME_DIR
        resolved_path = path.resolve()
        return resolved_path == HOME_DIR or HOME_DIR in resolved_path.parents
    except (ValueError, RuntimeError):
        return False


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024 or unit == 'TB':
            return f"{size_bytes:.2f} {unit}" if unit != 'B' else f"{size_bytes} {unit}"
        size_bytes /= 1024


def is_image_file(file_path: Path) -> bool:
    """Check if the file is an image based on its extension."""
    return file_path.suffix.lower() in IMAGE_EXTENSIONS


def is_text_file(file_path: Path) -> bool:
    """Check if the file is a text file based on its extension or MIME type."""
    return file_path.suffix.lower() in TEXT_FILE_EXTENSIONS

def get_file_content(file_path: Path) -> str:
    """
    Get the content of a text file as a string.
    
    Args:
        file_path: Path to the text file
    
    Returns:
        String content of the file
    """
    try:
        with open(file_path, 'r', errors='replace') as f:
            return f.read()
    except Exception:
        return "Error: Could not read file content"


def get_breadcrumbs(path: str):
    """Calculate breadcrumbs for navigation."""
    breadcrumbs = []
    current_path = ""
    parts = path.split("/") if path else []
    
    for part in parts:
        if not part:
            continue
        current_path = f"{current_path}/{part}"
        breadcrumbs.append({"name": part, "path": current_path})
    
    return breadcrumbs


def get_parent_path(path: str) -> str:
    """Determine parent directory URL."""
    if not path or path == "/":
        return "/"
    
    parent_parts = path.split("/")
    if len(parent_parts) <= 1:
        return "/"
    else:
        return "/" + "/".join(parent_parts[:-1])


def find_folder_description_file(folder_path: Path) -> tuple[Optional[Path], bool, Optional[str]]:
    """
    Find a description file for the folder in the parent directory.
    
    Returns a tuple of (file_path, is_image, file_path_for_url) where:
    - file_path is the Path to the description file or None if not found
    - is_image is a boolean indicating if the file is an image
    - file_path_for_url is the path as it should be used in URLs
    """
    if folder_path == HOME_DIR:
        return None, False, None
    
    folder_name = folder_path.name
    parent_dir = folder_path.parent
    
    # Look for any file that has the folder name as its base name
    potential_files = [f for f in parent_dir.iterdir() 
                      if f.is_file() and f.stem == folder_name]
    
    if not potential_files:
        return None, False, None
    
    # Prioritize .card files, then text files, then images
    for ext in ['.card', '.md', '.txt']:
        for file in potential_files:
            if file.suffix.lower() == ext:
                rel_path = file.relative_to(HOME_DIR)
                return file, False, f"/{rel_path}"
    
    # Then check for any text file
    for file in potential_files:
        if file.suffix.lower() in TEXT_FILE_EXTENSIONS:
            rel_path = file.relative_to(HOME_DIR)
            return file, False, f"/{rel_path}"
    
    # Finally check for images
    for file in potential_files:
        if file.suffix.lower() in IMAGE_EXTENSIONS:
            rel_path = file.relative_to(HOME_DIR)
            return file, True, f"/{rel_path}"
    
    # If we got here, there's no suitable file
    return None, False, None


@app.get("/raw/{path:path}")
async def get_raw_file(path: str = ""):
    """
    Serve raw file content, used for displaying images and downloading files.
    
    Args:
        path: The relative path from the home directory
        
    Returns:
        The raw file content with appropriate content type
    """
    if path.startswith("/"):
        path = path[1:]
    
    fs_path = HOME_DIR / path
    
    # Security check to prevent directory traversal
    if not is_safe_path(fs_path):
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Check if the path exists
    if not fs_path.exists() or not fs_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get MIME type
    content_type, encoding = mimetypes.guess_type(str(fs_path))
    content_type = content_type or "application/octet-stream"
    
    # Stream the file content
    def file_generator():
        with open(fs_path, 'rb') as file:
            yield from file
    
    return StreamingResponse(
        file_generator(),
        media_type=content_type
    )


@app.get("/{path:path}", response_class=HTMLResponse)
async def browse_path(request: Request, path: str = ""):
    """
    Serve files and directories from the user's home directory.
    
    Args:
        request: The FastAPI request object
        path: The relative path from the home directory
    
    Returns:
        - HTML directory listing for directories with inline previews
        - HTML page with file content for files
        - 404 if the path doesn't exist
        - 403 if the path is outside the home directory
    """
    # Normalize the requested path
    if path.startswith("/"):
        path = path[1:]
    
    # Construct the actual filesystem path
    fs_path = HOME_DIR / path
    
    # Security check to prevent directory traversal
    if not is_safe_path(fs_path):
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Check if the path exists
    if not fs_path.exists():
        raise HTTPException(status_code=404, detail="Path not found")
    
    # Calculate breadcrumbs and parent directory for any type of path
    breadcrumbs = get_breadcrumbs(path)
    parent_path = get_parent_path(path)
    
    # If it's a directory, list its contents
    if fs_path.is_dir():
        # Look for a description file for this folder
        folder_desc_file, is_desc_image, desc_file_path = find_folder_description_file(fs_path)
        folder_description = None
        folder_description_filename = None
        
        if folder_desc_file:
            folder_description_filename = folder_desc_file.name
            if is_desc_image:
                folder_description = ""  # We'll display the image directly in the template
            else:
                folder_description = get_file_content(folder_desc_file)
        
        # Get directory contents
        items = []
        for item in fs_path.iterdir():
            # Skip hidden files/folders
            if item.name.startswith('.'):
                continue
                
            rel_path = item.relative_to(HOME_DIR)
            url_path = f"/{rel_path}"
            
            # Get file/directory metadata
            modified_time = item.stat().st_mtime
            modified = f"{modified_time:.0f}"  # Simple timestamp format
            
            is_image = False
            is_text = False
            full_content = None
            
            if item.is_file():
                if is_image_file(item):
                    is_image = True
                elif is_text_file(item):
                    is_text = True
                    # Get the full content for text files
                    try:
                        full_content = get_file_content(item)
                    except Exception:
                        full_content = "Error: Could not read file content"
            
            if item.is_dir():
                items.append({
                    "name": item.name,
                    "path": url_path,
                    "is_dir": True,
                    "is_image": False,
                    "is_text": False,
                    "full_content": None,
                    "size": "-",
                    "modified": modified
                })
            else:
                items.append({
                    "name": item.name,
                    "path": url_path,
                    "is_dir": False,
                    "is_image": is_image,
                    "is_text": is_text,
                    "full_content": full_content,
                    "size": format_size(item.stat().st_size),
                    "modified": modified
                })
        
        # Sort items: directories first, then files, each sorted alphabetically
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        
        # Render directory template
        return templates.TemplateResponse(
            "unified.html",
            {
                "request": request,
                "items": items,
                "is_directory": True,
                "current_path": f"/{path}" if path else "/",
                "breadcrumbs": breadcrumbs,
                "parent_path": parent_path,
                "folder_description": folder_description,
                "folder_description_filename": folder_description_filename,
                "folder_description_is_image": is_desc_image,
                "folder_description_path": desc_file_path
            }
        )
    
    # If it's a file, serve it
    elif fs_path.is_file():
        is_image = is_image_file(fs_path)
        is_text = is_text_file(fs_path) and not is_image
        file_content = get_file_content(fs_path) if is_text else None
        
        # Render file template
        return templates.TemplateResponse(
            "unified.html",
            {
                "request": request,
                "is_directory": False,
                "is_image": is_image,
                "is_text": is_text,
                "file_name": fs_path.name,
                "file_size": format_size(fs_path.stat().st_size),
                "file_content": file_content,
                "current_path": f"/{path}" if path else "/",
                "breadcrumbs": breadcrumbs,
                "parent_path": parent_path
            }
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4444)

# This implementation adds the ability to display a description file for a folder at the top of the
# directory listing. The functionality looks for a file in the parent directory with the same name as
# the current folder (plus an extension). It prioritizes .card files, followed by other text files, and 
# finally image files. The content is displayed in a styled panel above the directory listing.
#
# The key changes include:
# 1. Added the find_folder_description_file function to locate relevant files
# 2. Modified the browse_path route to check for folder description files when displaying directories
# 3. Updated the template to include a new styled section for the folder description
# 4. Added support for both text and image folder descriptions

"""
spec:

Modify the script so that it contains a new 
"""
