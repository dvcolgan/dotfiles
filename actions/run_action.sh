#!/bin/bash

# Define the actions directory
ACTIONS_DIR="$HOME/actions"

# Make sure the actions directory exists
if [ ! -d "$ACTIONS_DIR" ]; then
    echo "Error: Actions directory $ACTIONS_DIR does not exist"
    exit 1
fi

# Find all files in the actions directory, pipe to rofi, and capture the selection
SELECTED_SCRIPT=$(find "$ACTIONS_DIR" -type f -executable 2>/dev/null | \
  sort | \
  sed "s|^$ACTIONS_DIR/||" | \
  rofi -dmenu -i -p "Select action:")

# Check if user selected a script
if [ -n "$SELECTED_SCRIPT" ]; then
    # Construct the full path to the script
    SCRIPT_PATH="$ACTIONS_DIR/$SELECTED_SCRIPT"
    
    # Check if the selected file exists and is executable
    if [ -f "$SCRIPT_PATH" ] && [ -x "$SCRIPT_PATH" ]; then
        # Open a new Alacritty terminal and run the script
        alacritty -e bash -c "$SCRIPT_PATH; read -p 'Press Enter to close...'"
        
        echo "Executing: $SCRIPT_PATH"
    else
        echo "Error: $SCRIPT_PATH is not an executable file"
        exit 1
    fi
else
    echo "No action selected"
fi
