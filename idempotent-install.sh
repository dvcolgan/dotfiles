#!/usr/bin/env bash

set -o errexit -o errtrace -o nounset -o pipefail

cd "$HOME"

# Symlink home folder files
ln -s "$HOME/repos/dotfiles/home/bashrc" .bashrc
ln -s "$HOME/repos/dotfiles/home/Xmodmap"  .Xmodmap
ln -s "$HOME/repos/dotfiles/home/bash_aliases" .bash_aliases

cd "$HOME/.config/"

# Symlink .config folder directories
ln -s "$HOME/repos/dotfiles/bspwm/" .
ln -s "$HOME/repos/dotfiles/sxhkd/" .
ln -s "$HOME/repos/dotfiles/dunst/" .
ln -s "$HOME/repos/dotfiles/alacritty/" .

# Symlink some folders for better use in the home folder
ln -s "$HOME/repos/dotfiles/actions/" .
ln -s "$HOME/repos/dotfiles/templates/" .
ln -s "$HOME/repos/dotfiles/tools/" .
ln -s "$HOME/repos/dotfiles/nvim/" .


