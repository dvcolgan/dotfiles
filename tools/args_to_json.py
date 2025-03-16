#!/usr/bin/env python3

import json
import re
import sys


def _set_nested_value(target_dict: dict, key_path: list[str], value: any) -> None:
    """Helper function to set a value in a nested dictionary using a key path."""
    current = target_dict
    for key in key_path[:-1]:
        if key not in current:
            current[key] = {}
        elif not isinstance(current[key], dict):
            # Convert to dict if it's not already one (overriding)
            current[key] = {}
        current = current[key]

    # Set the final value
    current[key_path[-1]] = value


def parse_arguments() -> tuple[dict, list[str]]:
    """Parse command line arguments and return them as a dictionary and a list of positional args.


    Convert command line arguments to JSON

    Usage:
    args_to_json.py [options] [positional_arguments]

    This tool converts command line arguments to a JSON representation and prints it to stdout.
    Positional arguments are not included in the JSON but are printed to stderr.

    It handles various formats including:
    - Flags (--flag, -f)
    - Key-value pairs (--key=value, -k=value, --key value)
    - Nested structures via dot notation (--config.server.port=8000)

    Examples:
    args_to_json.py --name John --age 30 file1.txt file2.txt
    args_to_json.py --verbose --config.server.port=8000 --config.server.host=localhost
    """

    result = {}
    positional_args = []

    # Skip the script name
    args = sys.argv[1:]

    i = 0
    while i < len(args):
        arg = args[i]

        # Handle --key=value format
        if arg.startswith("--") and "=" in arg:
            key, value = arg[2:].split("=", 1)
            key_path = key.split(".")
            _set_nested_value(result, key_path, parse_value(value))

        # Handle -k=value format
        elif arg.startswith("-") and "=" in arg:
            key, value = arg[1:].split("=", 1)
            _set_nested_value(result, [key], parse_value(value))

        # Handle --key value format
        elif arg.startswith("--"):
            key = arg[2:]

            # Check if there's a next argument and it's not a flag
            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                value = args[i + 1]
                key_path = key.split(".")
                _set_nested_value(result, key_path, parse_value(value))
                i += 1  # Skip the next arg since we've consumed it
            else:
                # It's a flag without value
                key_path = key.split(".")
                _set_nested_value(result, key_path, True)

        # Handle -k value format
        elif arg.startswith("-") and len(arg) == 2:
            key = arg[1]

            # Check if there's a next argument and it's not a flag
            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                value = args[i + 1]
                _set_nested_value(result, [key], parse_value(value))
                i += 1  # Skip the next arg since we've consumed it
            else:
                # It's a flag without value
                _set_nested_value(result, [key], True)

        # Handle combined short flags like -abc (equivalent to -a -b -c)
        elif arg.startswith("-") and len(arg) > 2 and "=" not in arg:
            for char in arg[1:]:
                _set_nested_value(result, [char], True)

        # Handle positional arguments
        else:
            positional_args.append(arg)

        i += 1

    return result, positional_args


def parse_value(value_str: str) -> any:
    """Convert string values to appropriate types (int, float, bool, etc.)."""
    # Check for boolean values
    if value_str.lower() in ("true", "yes", "y"):
        return True
    if value_str.lower() in ("false", "no", "n"):
        return False

    # Check for None
    if value_str.lower() in ("none", "null"):
        return None

    # Check for integers
    if re.match(r"^-?\d+$", value_str):
        return int(value_str)

    # Check for floats
    if re.match(r"^-?\d+\.\d+$", value_str):
        return float(value_str)

    # Otherwise, return as string
    return value_str


def main() -> None:
    """Main function to parse arguments and output JSON."""
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    args_dict, positional_args = parse_arguments()

    # Print JSON to stdout
    json_output = json.dumps(args_dict, indent=2)
    print(json_output)

    # Print positional arguments to stderr
    if positional_args:
        print("Positional arguments:", file=sys.stderr)
        for arg in positional_args:
            print(f"  {arg}", file=sys.stderr)


if __name__ == "__main__":
    main()
