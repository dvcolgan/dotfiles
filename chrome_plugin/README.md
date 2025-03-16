# Card Creator Chrome Extension

A lightweight Chrome extension that captures bookmark events and creates cards by sending data to a local API endpoint. When a user creates a bookmark, it captures the page URL, title, and any selected text, then POSTs this data to create a new card.

## Features

- Listens for bookmark creation events in Chrome
- Captures current page URL and title
- Captures any text currently selected on the page
- Sends data to a local API endpoint (`http://localhost/api/cards/`)

## Installation

### Development Setup

1. Clone this repository
```bash
git clone [repository-url]
cd card-creator-extension
```

2. Load the extension in Chrome:
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" in the top right
   - Click "Load unpacked"
   - Select the directory containing this extension

### Structure

```
card-creator-extension/
├── manifest.json      # Extension configuration and permissions
├── background.js      # Main event listener and API integration
└── README.md         # This file
```

## How It Works

The extension operates entirely in the background and consists of two main components:

1. **Event Listener**: Monitors for bookmark creation using Chrome's bookmarks API
2. **Data Collection**: When a bookmark is created, collects:
   - URL from the bookmark
   - Page title from the active tab
   - Any currently selected text

### Data Format

The extension sends POST requests with this payload structure:

```json
{
  "src": "https://example.com",
  "title": "Page Title",
  "text": "Selected text if any"
}
```

## API Requirements

The extension expects a local API endpoint at `http://localhost/api/cards/` that:
- Accepts POST requests
- Handles JSON payloads
- Implements proper CORS headers to accept requests from the extension

## Permissions

The extension requires these Chrome permissions:
- `bookmarks`: To detect bookmark creation
- `tabs`: To access tab information
- `activeTab`: To access page content
- `host_permissions`: For localhost API access

## Development

### Making Changes

1. Modify code in `background.js` or `manifest.json`
2. Go to `chrome://extensions/`
3. Click the refresh icon on the extension card
4. Changes will be loaded immediately

### Common Modifications

- To change the API endpoint: Update the URL in `background.js`
- To modify the payload: Adjust the payload object in the bookmark listener
- To add permissions: Update the permissions array in `manifest.json`

### Debugging

1. Open Chrome DevTools for the background script:
   - Go to `chrome://extensions/`
   - Find the extension
   - Click "service worker" link
2. Use console.log statements in background.js to debug
3. Network tab shows API requests

## Future Improvements

Potential enhancements:

1. Add error handling UI
2. Support for custom API endpoints
3. Configuration options for payload format
4. Authentication support for API
5. Batch processing for multiple bookmarks