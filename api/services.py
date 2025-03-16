import json

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import (
    JSONResponse,
)
from pydantic import BaseModel, Field

# Get templates from the main app
from .templates import templates
from .utils import (
    Format,
    RequestedFormat,
    entity_database,
)

router = APIRouter()


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


@router.post("/actions/move_entity/", response_model=EntityResponse)
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
