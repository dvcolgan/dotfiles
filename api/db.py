import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError
from pydantic_xml import BaseXmlModel

from .files import (
    BinaryFileModel,
    CssFileModel,
    FileModel,
    HtmlFileModel,
    ImageFileModel,
    JavaScriptFileModel,
    JsonFileModel,
    MarkdownFileModel,
    PydanticXmlFileModel,
    PythonFileModel,
    TextFileModel,
    XmlFileModel,
    YamlFileModel,
)

T = TypeVar("T", bound=BaseModel)


class FileSystemDatabase:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.root_path.mkdir(parents=True, exist_ok=True)

        self.file_previews: dict[str, type[FileModel]] = {
            ".txt": TextFileModel,
            ".md": MarkdownFileModel,
            ".html": HtmlFileModel,
            ".htm": HtmlFileModel,
            ".py": PythonFileModel,
            ".css": CssFileModel,
            ".js": JavaScriptFileModel,
            ".json": JsonFileModel,
            ".yaml": YamlFileModel,
            ".yml": YamlFileModel,
            ".xml": XmlFileModel,
            ".jpg": ImageFileModel,
            ".jpeg": ImageFileModel,
            ".png": ImageFileModel,
            ".gif": ImageFileModel,
            ".svg": ImageFileModel,
        }

    def _resolve_path(self, path: Path) -> Path:
        if path.is_absolute():
            if not str(path).startswith(str(self.root_path)):
                raise ValueError(f"Path must be within database root: {self.root_path}")
            return path
        return self.root_path / path

    def _get_model_class(self, path: Path) -> type[FileModel]:
        suffix = path.suffix.lower()
        return self.file_previews.get(suffix, BinaryFileModel)

    def get(
        self, path: Path, model_class: type[BaseModel] | None = None
    ) -> FileModel | T:
        resolved_path = self._resolve_path(path)
        file_model_class = self._get_model_class(resolved_path)

        # Handle XML files with Pydantic models
        if (
            issubclass(file_model_class, XmlFileModel)
            and model_class
            and issubclass(model_class, BaseXmlModel)
        ):
            file_model = PydanticXmlFileModel.load(resolved_path, model_class)
        else:
            file_model = file_model_class.load(resolved_path)

        # If a model class is provided, validate and convert the content
        if model_class and not isinstance(file_model.content, model_class):
            try:
                # For JSON/YAML files, content is already a dict that can be parsed
                if isinstance(file_model, (JsonFileModel, YamlFileModel)):
                    validated_content = model_class.model_validate(file_model.content)
                # For text files, try to parse as JSON
                elif isinstance(file_model, TextFileModel):
                    try:
                        parsed_content = json.loads(file_model.content)
                        validated_content = model_class.model_validate(parsed_content)
                    except json.JSONDecodeError:
                        raise ValidationError(
                            [
                                {
                                    "loc": ("content",),
                                    "msg": "Invalid JSON content",
                                    "type": "value_error",
                                }
                            ],
                            model_class,
                        )
                else:
                    raise ValidationError(
                        [
                            {
                                "loc": ("content",),
                                "msg": f"Cannot validate {file_model.__class__.__name__} with {model_class.__name__}",
                                "type": "value_error",
                            }
                        ],
                        model_class,
                    )

                # Update the file model with validated content
                file_model.content = validated_content
            except ValidationError as e:
                raise ValidationError(
                    [
                        {
                            "loc": ("file", *err["loc"]),
                            "msg": err["msg"],
                            "type": err["type"],
                        }
                        for err in e.errors()
                    ],
                    model_class,
                )

        return file_model

    def set(
        self,
        path: Path,
        content: str | dict | bytes | BaseXmlModel | ET.Element | BaseModel,
    ) -> FileModel:
        resolved_path = self._resolve_path(path)
        model_class = self._get_model_class(resolved_path)

        # Handle Pydantic models (XML and regular)
        if isinstance(content, BaseModel):
            if isinstance(content, BaseXmlModel):
                model = PydanticXmlFileModel(
                    filename=resolved_path.name,
                    path=resolved_path,
                    content=content,
                    model_class=type(content),
                )
            else:
                # For regular Pydantic models, serialize to appropriate format based on file extension
                if model_class == JsonFileModel:
                    model = JsonFileModel(
                        filename=resolved_path.name,
                        path=resolved_path,
                        content=content.model_dump(),
                    )
                elif model_class in (YamlFileModel,):
                    model = YamlFileModel(
                        filename=resolved_path.name,
                        path=resolved_path,
                        content=content.model_dump(),
                    )
                else:
                    # Default to JSON serialization for text formats
                    model = TextFileModel(
                        filename=resolved_path.name,
                        path=resolved_path,
                        content=json.dumps(content.model_dump(), indent=2),
                    )
        # Handle raw ElementTree Element for XML files
        elif model_class == XmlFileModel and isinstance(content, ET.Element):
            model = XmlFileModel(
                filename=resolved_path.name, path=resolved_path, content=content
            )
        # Handle content based on appropriate model type
        elif isinstance(content, str) and issubclass(model_class, TextFileModel):
            model = model_class(
                filename=resolved_path.name, path=resolved_path, content=content
            )
        # Handle dict content for JSON/YAML
        elif isinstance(content, dict) and (
            model_class == JsonFileModel or model_class == YamlFileModel
        ):
            model = model_class(
                filename=resolved_path.name, path=resolved_path, content=content
            )
        # Handle binary content
        elif isinstance(content, bytes):
            model = BinaryFileModel(
                filename=resolved_path.name, path=resolved_path, content=content
            )
        # Unable to determine appropriate model
        else:
            raise TypeError(
                f"Content type {type(content)} not compatible with file type {model_class.__name__}"
            )

        model.save()
        return model

    def exists(self, path: Path) -> bool:
        resolved_path = self._resolve_path(path)
        return resolved_path.exists()

    def delete(self, path: Path) -> bool:
        resolved_path = self._resolve_path(path)

        if not resolved_path.exists():
            return False

        resolved_path.unlink()
        return True

    def list_files(
        self, directory: Path | None = None, pattern: str = "*"
    ) -> list[Path]:
        if directory is None:
            base_path = self.root_path
        else:
            base_path = self._resolve_path(directory)

        if not base_path.exists() or not base_path.is_dir():
            return []

        return [
            p.relative_to(self.root_path)
            for p in base_path.glob(pattern)
            if p.is_file()
        ]

    def list_directory(self, path: Path) -> list[FileModel]:
        """List directory contents with file models"""
        resolved_path = self._resolve_path(path)

        if not resolved_path.exists() or not resolved_path.is_dir():
            return []

        items = []
        for item in resolved_path.iterdir():
            try:
                # Only load file_model for files, not directories
                if item.is_file():
                    try:
                        model_class = self._get_model_class(item)
                        file_model = model_class.load(item)
                        items.append(file_model)
                    except Exception:
                        # If we can't load the file model, proceed without it
                        pass
                else:
                    # For directories, we create a special type of FileModel
                    # This could be extended to create a DirectoryModel class
                    # but for now we'll work with what we have
                    stat_info = item.stat()
                    metadata = FileModel(
                        filename=item.name,
                        path=item,
                        content=None,
                    )
                    metadata.is_dir = True  # Add directory flag
                    items.append(metadata)
            except (FileNotFoundError, PermissionError):
                # Handle errors gracefully
                pass

        # Sort items - directories first, then files
        items.sort(key=lambda x: (not getattr(x, "is_dir", False), x.filename.lower()))
        return items

    def get_breadcrumbs(self, path: Path) -> list[dict]:
        """Generate breadcrumb navigation for a path"""
        resolved_path = self._resolve_path(path)
        parts = resolved_path.parts

        # Start with root relative to database root
        breadcrumbs = []
        current_path = ""

        # Build path incrementally
        for part in parts:
            if not part:  # Handle root directory
                breadcrumbs.append({"name": "root", "path": "/"})
                current_path = "/"
            else:
                current_path = os.path.join(current_path, part)
                breadcrumbs.append({"name": part, "path": current_path})

        return breadcrumbs
