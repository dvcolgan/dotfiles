#!/usr/bin/env python

import os
import re
import subprocess
from pathlib import Path
from typing import Optional

def run_command(cmd: list) -> Optional[str]:
    try:
        return subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError:
        return None

def find_cards_by_score():
    cmd = ["rg", r"^#.*\^(\d+).*$", str(Path.home() / 'recursive_root'), "-n", "--no-heading"]
    
    output = run_command(cmd)
    if not output:
        return
    
    results = []
    for line in output.splitlines():
        file_path, line_num, content = line.split(':', 2)
        score_match = re.search(r'\^(\d+)', content)
        if score_match:
            score = int(score_match.group(1))
            results.append((score, f"{file_path}:{line_num}:{content}"))
    
    sorted_results = sorted(results, key=lambda x: x[0], reverse=True)
    results = []
    for _, result in sorted_results:
        results.append(result)
    return results

def top_cards():
    return find_cards_by_score()

if __name__ == "__main__":
    for result in top_cards():
        print(result)
