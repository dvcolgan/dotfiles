# Recursive Garden

A modern implementation of the Zettelkasten note-taking system, designed to make knowledge management as engaging as social media.

## Overview

Recursive Garden is a dynamic knowledge management system that combines elements of Zettelkasten system with UI patterns from popular social platforms. The application allows for:

- **Recursive Note Organization**: Cards can be nested arbitrarily deep, allowing for complex knowledge hierarchies
- **Multiple Organization Methods**:
  - Spatial organization on an infinite 2D canvas
  - Parent-child relationships for hierarchical organization
  - Tagging for associative connections
  - Sequential ordering between cards
  - Reddit-style voting and ranking
  - Topic-based organization similar to subreddits
- **Engagement-Driven Design**: Incorporates proven engagement patterns from social media platforms (YouTube, Reddit, Twitter) but redirects them toward productive knowledge work
- **Hybrid Frontend Architecture**: Combines the best of server-side rendering and dynamic client-side interactions

### Design Philosophy

- **Speed First**: Every feature is implemented with performance in mind, ensuring near-instantaneous response times
- **Productive Engagement**: Uses "hook" patterns (trigger → action → reward → investment) to encourage writing and knowledge organization
- **Seamless Experience**: Smooth transitions between static and dynamic content
- **Spatial Thinking**: Leverages human spatial memory by allowing notes to be organized in a 2D space

## Tech Stack

### Backend
- Python 3.13+
- Django 5.1+
- Django REST Framework
- Django Slippers for component-based templates
- PostgreSQL/SQLite for data storage

### Frontend
- Vue.js 3
- TypeScript
- Tailwind CSS
- Vite build system
- Transform-based infinite canvas

### Integration
- Django Vite for backend/frontend integration
- HTMX for enhanced server-rendered interactions
- REST API for dynamic data operations

## Development

### Prerequisites
- Python 3.13 or higher
- Node.js (Latest LTS version recommended)
- PostgreSQL (optional, SQLite supported by default)

See the [docs/](docs/) directory for detailed documentation on specific features.