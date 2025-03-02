#!/bin/bash

# Function to show usage
show_usage() {
    echo "Usage: $0 [text] [prompt_name]"
    echo "  text: Input text (required)"
    echo "  prompt_name: Optional - name of the prompt file in ~/prompts/ without extension"
    echo "  Accepts input either as an argument or from stdin, or both"
    exit 1
}

# Set default prompt name
PROMPT_NAME="system"

# Check if we have a second argument for prompt name
if [ $# -eq 2 ]; then
    PROMPT_NAME="$2"
fi

# Find prompt file - look for common extensions
PROMPT_DIR="$HOME/prompts"
PROMPT_FILE=""

for ext in md txt yaml yml json; do
    if [ -f "$PROMPT_DIR/$PROMPT_NAME.$ext" ]; then
        PROMPT_FILE="$PROMPT_DIR/$PROMPT_NAME.$ext"
        break
    fi
done

# Check if prompt file exists
if [ -z "$PROMPT_FILE" ]; then
    echo "Error: Prompt file not found at $PROMPT_DIR/$PROMPT_NAME.*"
    exit 1
fi

# Initialize INPUT as empty
INPUT=""

# Check if we have input from stdin
if [ ! -t 0 ]; then  # If stdin is not a terminal (pipe or redirect)
    STDIN_CONTENT=$(cat)
    INPUT=$(printf "\n<existing_script>\n%s\n</existing_script>" "${STDIN_CONTENT}")
fi

# Check if we have an argument
if [ $# -gt 0 ]; then
    # If we already have stdin content, add two newlines before the argument
    if [ -n "$INPUT" ]; then
        INPUT="${INPUT}\n\n$1"
    else
        INPUT="$1"
    fi
elif [ -z "$INPUT" ]; then  # No argument and no stdin
    show_usage
fi

# Read the system prompt from file
SYSTEM_PROMPT="$(render_template.py "$PROMPT_FILE")"

# Uncomment to debug prompts
#echo -e "$INPUT"
#echo -e "$SYSTEM_PROMPT"

# Run llm with the system prompt and combined input
echo -e "$INPUT" | llm --system "$SYSTEM_PROMPT"
