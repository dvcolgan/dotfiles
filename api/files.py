import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, Optional, TypeVar

import yaml
from pydantic import BaseModel, ConfigDict, Field
from pydantic_xml import BaseXmlModel

T = TypeVar("T", bound=BaseModel)


class FileMetadata(BaseModel):
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)
    size: int = 0
    mime_type: str = ""


class FileModel(BaseModel):
    filename: str
    path: Path
    metadata: FileMetadata = Field(default_factory=FileMetadata)
    content: Any
    mime_type: ClassVar[str] = "application/octet-stream"
    template_name: ClassVar[str] = "file_previews/unknown.html"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def load(cls, path: Path) -> "FileModel":
        raise NotImplementedError("Subclass must implement load method")

    def save(self) -> None:
        raise NotImplementedError("Subclass must implement save method")

    @classmethod
    def get_mime_type(cls) -> str:
        return cls.mime_type

    def get_template_name(self) -> str:
        """Returns the template used to render this file type"""
        return self.template_name

    def get_display_content(self) -> Any:
        """Returns content prepared for display in templates"""
        return self.content

    def get_preview_content(self) -> Any:
        """Returns truncated content for preview displays"""
        content = self.get_display_content()
        if isinstance(content, str) and len(content) > 10240:
            return content[:10240] + "\n... (content truncated)"
        return content

    def get_file_extension(self) -> str:
        return self.path.suffix.lstrip(".")


class TextFileModel(FileModel):
    content: str = ""
    mime_type: ClassVar[str] = "text/plain"
    template_name: ClassVar[str] = "file_previews/txt.html"

    @classmethod
    def load(cls, path: Path) -> "TextFileModel":
        if not path.exists():
            return cls(filename=path.name, path=path, content="")

        stats = path.stat()
        metadata = FileMetadata(
            created=datetime.fromtimestamp(stats.st_ctime),
            modified=datetime.fromtimestamp(stats.st_mtime),
            size=stats.st_size,
            mime_type=cls.get_mime_type(),
        )

        content = path.read_text(encoding="utf-8")

        return cls(filename=path.name, path=path, metadata=metadata, content=content)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata.modified = datetime.now()
        self.path.write_text(self.content, encoding="utf-8")
        self.metadata.size = self.path.stat().st_size


class MarkdownFileModel(TextFileModel):
    mime_type: ClassVar[str] = "text/markdown"
    template_name: ClassVar[str] = "file_previews/md.html"


class HtmlFileModel(TextFileModel):
    mime_type: ClassVar[str] = "text/html"
    # Use text template for HTML to escape content


class CodeFileModel(TextFileModel):
    """Base class for all code file types"""

    template_name: ClassVar[str] = "file_previews/code.html"


class PythonFileModel(CodeFileModel):
    mime_type: ClassVar[str] = "text/x-python"


class CssFileModel(CodeFileModel):
    mime_type: ClassVar[str] = "text/css"


class JavaScriptFileModel(CodeFileModel):
    mime_type: ClassVar[str] = "application/javascript"


class StructuredDataFileModel(FileModel):
    """Base class for structured data files (JSON, YAML)"""

    content: dict[str, Any] = Field(default_factory=dict)

    def get_display_content(self) -> str:
        """Returns formatted data string"""
        raise NotImplementedError("Subclass must implement get_display_content method")


class JsonFileModel(StructuredDataFileModel):
    mime_type: ClassVar[str] = "application/json"
    template_name: ClassVar[str] = "file_previews/json.html"

    @classmethod
    def load(cls, path: Path) -> "JsonFileModel":
        if not path.exists():
            return cls(filename=path.name, path=path, content={})

        stats = path.stat()
        metadata = FileMetadata(
            created=datetime.fromtimestamp(stats.st_ctime),
            modified=datetime.fromtimestamp(stats.st_mtime),
            size=stats.st_size,
            mime_type=cls.get_mime_type(),
        )

        content = json.loads(path.read_text(encoding="utf-8"))

        return cls(filename=path.name, path=path, metadata=metadata, content=content)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata.modified = datetime.now()
        self.path.write_text(json.dumps(self.content, indent=2), encoding="utf-8")
        self.metadata.size = self.path.stat().st_size

    def get_display_content(self) -> str:
        """Returns formatted JSON string"""
        return json.dumps(self.content, indent=2)


class YamlFileModel(StructuredDataFileModel):
    mime_type: ClassVar[str] = "application/yaml"

    @classmethod
    def load(cls, path: Path) -> "YamlFileModel":
        if not path.exists():
            return cls(filename=path.name, path=path, content={})

        stats = path.stat()
        metadata = FileMetadata(
            created=datetime.fromtimestamp(stats.st_ctime),
            modified=datetime.fromtimestamp(stats.st_mtime),
            size=stats.st_size,
            mime_type=cls.get_mime_type(),
        )

        content = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

        return cls(filename=path.name, path=path, metadata=metadata, content=content)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata.modified = datetime.now()
        self.path.write_text(
            yaml.dump(self.content, default_flow_style=False), encoding="utf-8"
        )
        self.metadata.size = self.path.stat().st_size

    def get_display_content(self) -> str:
        """Returns formatted YAML string"""
        return yaml.dump(self.content, default_flow_style=False)


class XmlFileModel(FileModel):
    content: Optional[ET.Element] = None
    mime_type: ClassVar[str] = "application/xml"

    @classmethod
    def load(cls, path: Path) -> "XmlFileModel":
        if not path.exists():
            root = ET.Element("root")
            return cls(filename=path.name, path=path, content=root)

        stats = path.stat()
        metadata = FileMetadata(
            created=datetime.fromtimestamp(stats.st_ctime),
            modified=datetime.fromtimestamp(stats.st_mtime),
            size=stats.st_size,
            mime_type=cls.get_mime_type(),
        )

        tree = ET.parse(path)
        root = tree.getroot()

        return cls(filename=path.name, path=path, metadata=metadata, content=root)

    def save(self) -> None:
        if self.content is None:
            raise ValueError("XML content cannot be None")

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata.modified = datetime.now()
        tree = ET.ElementTree(self.content)
        tree.write(self.path, encoding="utf-8", xml_declaration=True)
        self.metadata.size = self.path.stat().st_size

    def get_display_content(self) -> str:
        """Returns formatted XML string"""
        if self.content is None:
            return ""

        xml_str = ET.tostring(self.content, encoding="utf-8", method="xml")
        try:
            # Try to import xml.dom.minidom for pretty-printing
            from xml.dom import minidom

            return minidom.parseString(xml_str).toprettyxml(indent="  ")
        except ImportError:
            # Fall back to raw XML if minidom is not available
            return xml_str.decode("utf-8")


class PydanticXmlFileModel(FileModel):
    content: Optional[BaseXmlModel] = None
    model_class: Optional[type[BaseXmlModel]] = None
    mime_type: ClassVar[str] = "application/xml"

    @classmethod
    def load(
        cls, path: Path, model_class: type[BaseXmlModel]
    ) -> "PydanticXmlFileModel":
        if not path.exists():
            return cls(
                filename=path.name,
                path=path,
                content=model_class.model_construct(),
                model_class=model_class,
            )

        stats = path.stat()
        metadata = FileMetadata(
            created=datetime.fromtimestamp(stats.st_ctime),
            modified=datetime.fromtimestamp(stats.st_mtime),
            size=stats.st_size,
            mime_type=cls.get_mime_type(),
        )

        xml_content = path.read_bytes()
        content = model_class.from_xml(xml_content)

        return cls(
            filename=path.name,
            path=path,
            metadata=metadata,
            content=content,
            model_class=model_class,
        )

    def save(self) -> None:
        if self.content is None:
            raise ValueError("XML content cannot be None")

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata.modified = datetime.now()
        xml_content = self.content.to_xml(
            pretty_print=True, encoding="utf-8", xml_declaration=True
        )
        self.path.write_bytes(xml_content)
        self.metadata.size = self.path.stat().st_size

    def get_display_content(self) -> str:
        """Returns formatted XML string"""
        if self.content is None:
            return ""

        xml_content = self.content.to_xml(pretty_print=True, encoding="utf-8")
        return xml_content.decode("utf-8")


class BinaryFileModel(FileModel):
    content: bytes = b""
    mime_type: ClassVar[str] = "application/octet-stream"

    @classmethod
    def load(cls, path: Path) -> "BinaryFileModel":
        if not path.exists():
            return cls(filename=path.name, path=path, content=b"")

        stats = path.stat()
        metadata = FileMetadata(
            created=datetime.fromtimestamp(stats.st_ctime),
            modified=datetime.fromtimestamp(stats.st_mtime),
            size=stats.st_size,
            mime_type=cls.get_mime_type(),
        )

        content = path.read_bytes()

        return cls(filename=path.name, path=path, metadata=metadata, content=content)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata.modified = datetime.now()
        self.path.write_bytes(self.content)
        self.metadata.size = self.path.stat().st_size

    def get_template_name(self) -> str:
        """Determine template based on mime type"""
        mime_type = self.metadata.mime_type
        if mime_type.startswith("image/"):
            return "file_previews/image.html"
        return "file_previews/txt.html"  # Binary files just show size

    def get_display_content(self) -> str:
        """For binary files, we just return a placeholder message"""
        return f"Binary file, {self.metadata.size} bytes"


class ImageFileModel(BinaryFileModel):
    mime_type: ClassVar[str] = "image/*"  # Generic image type
    template_name: ClassVar[str] = "file_previews/image.html"
