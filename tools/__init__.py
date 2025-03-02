from pydantic import BaseModel

"""
Given a python function, generate the openapi spec that would be useable by Claude

also make it so that i can call the function in a web browser with a form,
and also from the command line with arguments

command line arguments are args, command line flags are kwargs

formdata is all kwargs

use fastapi to receive these

"""

class TextBlock(BaseModel):


This section will list all the supported block types, such as text, image, file, code, markdown, table, html, audio, and video.

class ToolInputSchema(BaseModel):


class RecursiveTool(BaseModel):
    name: str
    description: str
    input_schema: ToolInputSchema

