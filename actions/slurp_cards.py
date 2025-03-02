#!/usr/bin/env python

import sys
import click
from actions.create_card import create_card

def slurp_cards(text):
    """
    Takes input text and creates cards using the create_card function
    
    Args:
        text (str): The input text to process
        
    Returns:
        The result from create_card function
    """
    return create_card(text)

@click.command()
def cli():
    """
    Command line interface for slurp_cards.
    Reads from stdin and passes the text to slurp_cards function.
    """
    # Read from stdin
    text = sys.stdin.read()
    
    # Call slurp_cards with the input text
    result = slurp_cards(text)
    
    # Print the result
    print(result)

if __name__ == '__main__':
    cli()
