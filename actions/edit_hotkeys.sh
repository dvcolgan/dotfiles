#!/bin/bash

# Script to open sxhkdrc in Neovim using Alacritty
# When Neovim is closed, the terminal will also close

alacritty -e bash -c "nvim ~/.config/sxhkd/sxhkdrc && pkill -USR1 -x sxhkd; notify-send 'updated hotkeys'; exit" &
