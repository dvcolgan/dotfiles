import sys
import traceback

import jinja2
from rich.console import Console
from rich.traceback import Traceback

from .settings import BASE_DIR

console = Console()


_loader = jinja2.FileSystemLoader(BASE_DIR / "templates")
_env = jinja2.Environment(loader=_loader, autoescape=False)
_components = {}


def render(template_name: str, **context) -> str:
    try:
        return _env.get_template(template_name).render(**context)
    except Exception as e:
        exc_type, exc_value, tb = sys.exc_info()
        rich_traceback = Traceback.extract(exc_type, exc_value, tb)
        with console.capture():
            console.print(rich_traceback)

        # Capture the traceback using the traceback module
        formatted_traceback = "".join(
            traceback.format_exception(exc_type, exc_value, tb)
        )

        error_context = {
            "error_message": str(e),
            "template_name": template_name,
            "context": context,
            "stack_trace": formatted_traceback,
        }
        return _env.get_template("errors/error_page.html").render(**error_context)


def render_from_string(template_string: str, **context) -> str:
    try:
        return _env.from_string(template_string).render(**context)
    except Exception as e:
        exc_type, exc_value, tb = sys.exc_info()
        rich_traceback = Traceback.extract(exc_type, exc_value, tb)
        with console.capture():
            console.print(rich_traceback)

        raise e

        ## Capture the traceback using the traceback module
        # formatted_traceback = "".join(traceback.format_exception(exc_type, exc_value, tb))
        #
        # error_context = {
        #    'error_message': str(e),
        #    'template_string': template_string,
        #    'context': context,
        #    'stack_trace': formatted_traceback
        # }
        # return _env.get_template('errors/rendering_error.html').render(**error_context)
