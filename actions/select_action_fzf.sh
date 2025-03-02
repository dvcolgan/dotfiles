#!/bin/bash


script_path=$(fd . actions/ --color=always | fzf --ansi)
if [ -n "$script_path" ]; then
    "$script_path"
fi
