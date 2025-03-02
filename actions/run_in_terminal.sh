#!/bin/bash

# Check if an argument was provided
if [ $# -gt 0 ]; then
    command_to_run="$1"
else
    # If no argument, read from stdin
    read -t 0 && command_to_run=$(cat)
    
    # If nothing from stdin either, exit with error
    if [ -z "$command_to_run" ]; then
        echo "Error: No command provided via argument or stdin" >&2
        exit 1
    fi
fi

# Execute the command in alacritty
alacritty -e bash -c "$command_to_run"
