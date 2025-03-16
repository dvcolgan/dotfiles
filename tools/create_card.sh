#!/bin/bash


# Ask for filename using zenity
filename=$(zenity --entry --title="Create New Card" --text="Enter filename:")

# Check if user cancelled the dialog
if [ -z "$filename" ]; then
    exit 0
fi

# Create full path
filepath=~/recursive_root/"${filename}.card"

# Check if template exists
template=~/templates/new_card.card
if [ ! -f "$template" ]; then
    zenity --error --text="Template file not found at: $template"
    exit 1
fi

render_template.py "$template" >> "$filepath"

edit_in_terminal.sh "$filepath"


# Default values
TITLE="hello"
TEXT="world"
URL="http://localhost/api/cards/"
CLIENT="httpie"  # Default client
# Create JSON payload using args_to_json.py
JSON_PAYLOAD=$(./scripts/args_to_json.py --title "$TITLE" --text "$TEXT")

echo "Submitting card to $URL with payload:"
echo "$JSON_PAYLOAD"
echo "Using client: $CLIENT"

# Send the request using the selected HTTP client
curl -X POST "$URL" \
    -H "Content-Type: application/json" \
    -d "$JSON_PAYLOAD"

echo "Request sent successfully!"