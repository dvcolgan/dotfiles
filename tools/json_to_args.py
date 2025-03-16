#!/usr/bin/env python3

import json
import sys

import click


def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """Flatten a nested dictionary into a flat dictionary with dot notation keys."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def format_value(value: any) -> str:
    """Format a value based on its type for command line representation."""
    if value is True:
        return ""  # For flags
    elif value is False:
        # Skip False values completely
        return None
    elif value is None:
        return "null"
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        # Quote strings if they contain spaces
        value_str = str(value)
        if " " in value_str or not value_str:
            return f'"{value_str}"'
        return value_str


def json_to_args(json_data: dict) -> str:
    """Convert JSON data to command-line arguments string."""
    # Flatten the nested dict
    flat_dict = flatten_dict(json_data)

    args = []
    for key, value in flat_dict.items():
        formatted_value = format_value(value)
        if formatted_value is None:  # Skip False values
            continue

        # For boolean True, just add the flag
        if formatted_value == "":
            args.append(f"--{key}")
        else:
            # Use --key=value format for all other types
            args.append(f"--{key}={formatted_value}")

    return " ".join(args)


@click.command(
    help="Convert JSON to command line arguments. "
    "Accepts JSON input either from a file or from stdin."
)
@click.argument("file", type=click.File("r"), required=False)
@click.option(
    "--compact",
    "-c",
    is_flag=True,
    help="Output arguments in a compact form without newlines",
)
@click.option(
    "--output",
    "-o",
    type=click.File("w"),
    default="-",
    help="Output file (default: stdout)",
)
def main(file, compact, output):
    """Convert JSON to command line arguments.

    If FILE is not provided, reads from stdin.
    """
    try:
        # Read from file or stdin
        if file:
            json_data = json.load(file)
        else:
            # Check if there's data in stdin
            if sys.stdin.isatty():
                click.echo(
                    "Error: No input provided. Provide a file or pipe JSON data.",
                    err=True,
                )
                click.echo("Run with --help for more information.", err=True)
                sys.exit(1)
            json_data = json.load(sys.stdin)

        # Convert JSON to args
        args_string = json_to_args(json_data)

        # Output result
        if not compact and output.name == "<stdout>":
            # Format for better terminal viewing when not in compact mode
            args_list = args_string.split(" ")
            click.echo("\n".join(args_list), file=output)
        else:
            click.echo(args_string, file=output)

    except json.JSONDecodeError:
        click.echo("Error: Input does not contain valid JSON.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
