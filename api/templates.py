from pathlib import Path

from fastapi.templating import Jinja2Templates

from .settings import BASE_DIR

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Add Path to global template context
templates.env.globals["Path"] = Path

# Add custom filters
templates.env.filters["datetime"] = lambda timestamp: timestamp
