#!/usr/bin/env python

from core.schemas import Card

render_formats = ['markdown', 'yaml', 'json', 'html']


def render_card(card: Card, format="markdown") -> str:
    card.render()
    for child in card.children:
        render_card(child)
