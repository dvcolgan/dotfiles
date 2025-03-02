#!/usr/bin/env bash

set -o errexit -o errtrace -o nounset -o pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

echo "I am currently in $(pwd)."

cp -v ./vconsole.conf /etc/vconsole.conf
cp -v ./dvorak-with-tweaks.map /usr/share/kbd/keymaps/i386/dvorak/

#cp ./tmux.conf "$HOME/.tmux.conf"
#cp ./bashrc "$HOME/.tmux.conf"
