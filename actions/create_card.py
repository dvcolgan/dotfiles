#!/usr/bin/env python


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

alacritty -e nvim "+normal Go" "$filepath"
