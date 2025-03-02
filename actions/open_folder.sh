#!/bin/bash

# Define the home directory
HOME_DIR="$HOME"

# Find all directories, pipe directly to rofi, and capture the selection
SELECTED_PATH=$(find "$HOME_DIR" -type d -not -path "*/\.*" 2>/dev/null | \
  awk '{print length, $0}' | \
  sort -n | \
  cut -d' ' -f2- | \
  sed "s|^$HOME_DIR/||" | \
  rofi -dmenu -i -p "Select folder:")

# Check if user selected a folder
if [ -n "$SELECTED_PATH" ]; then
    # Format the URL
    if [ -z "$SELECTED_PATH" ]; then
        # If the selection is empty or just the home directory
        URL="localhost:4444/"
    else
        URL="localhost:4444/$SELECTED_PATH"
    fi
    
    # Open Brave browser in app mode with the selected URL
    brave-browser --app="http://$URL"
    
    echo "Opening: http://$URL"
else
    echo "No folder selected"
fi
