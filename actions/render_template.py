#!/usr/bin/env python

from datetime import datetime
import sys
import click
from jinja2 import Template
import ast

def render_template(template, context):
    return

def parse_defines(defines):
    context = {}
    for definition in defines:
        if '=' in definition:
            key, value = definition.split('=', 1)
            try:
                # Try to evaluate as Python literal
                value = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                # If that fails, treat as string
                pass
            context[key.strip()] = value
    return context

@click.command(help='Process text through Jinja2 templating engine')
@click.argument('file', type=click.File('r'), default='-')
@click.option('-D', '--define', multiple=True, help='Define template variables in the format KEY=VALUE')
def main(file, define):
    # Read input text
    template_text = file.read()
    if file is not sys.stdin:
        file.close()

    # Parse template variables from command line
    context = parse_defines(define)

    # Add a timestamp
    context['timestamp'] = datetime.now().strftime('%Y%m%d%H%M%S')

    # Create and render template
    template = Template(template_text)
    result = template.render(**context)

    # Output result
    click.echo(result, nl=False)

if __name__ == '__main__':
    main()
