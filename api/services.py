from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .utils import entity_database

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
