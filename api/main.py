from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import settings
from .selectors import router as selectors_router
from .services import router as services_router

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory=settings.BASE_DIR / "static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory=settings.BASE_DIR / "templates")

# Add Path to global template context
templates.env.globals["DEBUG"] = settings.DEBUG
templates.env.filters["datetime"] = lambda timestamp: timestamp

# Include routers from other modules
app.include_router(services_router)
app.include_router(selectors_router)
