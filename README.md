# X (Twitter) Utilities

A collection of utilities for interacting with X (formerly Twitter) using Python and Playwright.

## Features

- Automated login handling with cookie persistence
- Profile page navigation
- Layout discovery and analysis
- Screenshot capture for reference
- Structured data extraction (coming soon)

## Prerequisites

- Python 3.11+
- Playwright
- Chrome/Chromium browser

## Installation

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd x_utilities
   ```

2. Create and activate a virtual environment:

   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:

   ```bash
   python -m playwright install chromium
   ```

## Configuration

1. Copy the example cookies file:

   ```bash
   cp cookies.json.example cookies.json
   ```

2. Update `config.py` with your settings:
   - `PROFILE_USERNAME`: Your X profile username
   - `HEADLESS`: Set to `True` for headless browser operation
   - Adjust timeouts if needed

## How to Get Your Auth Cookie

1. **Log in via Your Browser:**
   Open your preferred browser (e.g. Chrome) and navigate to <https://x.com>. Log in to your account manually.

2. **Open Developer Tools:**
   Press F12 (or right‑click on the page and choose "Inspect") to open the Developer Tools.

3. **Go to the Application (or Storage) tab.**

4. **Locate Cookies:**
   In the sidebar, expand Cookies and select the domain (usually "x.com" or "twitter.com" if you still see that in legacy settings).

5. **Export Cookies:**
   - Install the [Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/iphcomljdfghbkdcfndaijbokpgddeno) extension
   - Click the extension icon while on X.com
   - Click "Export" and save as `cookies.json` in the project directory

## Usage

### Basic Usage

Run the main script:

```bash
python main.py
```

This will:

1. Create necessary directories
2. Handle login (using cookies or manual login if needed)
3. Navigate to the specified profile
4. Perform layout discovery if needed

### Components

- `main.py`: Main entry point and program flow
- `login_x.py`: Login and session management
- `discover.py`: Layout analysis and screenshot capture
- `config.py`: Configuration settings

### Output

The script creates a `config` directory containing:

- `layout.json`: Discovered page structure and elements
- `screenshots/`: Timestamped screenshots of analyzed pages
- `cookies.json`: Saved authentication cookies

## Development

### Project Structure

```txt
x_utilities/
├── config/                 # Created on first run
│   ├── layout.json        # Discovered layout data
│   └── screenshots/       # Page screenshots
├── config.py              # Configuration settings
├── login_x.py            # Login handling
├── discover.py           # Layout discovery
├── main.py              # Main program
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Adding New Features

1. Update configuration in `config.py`
2. Add new functionality in appropriate module
3. Import and orchestrate from `main.py`

## Coming Soon

- Tweet scraping functionality
- Data export options
- More analysis tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your chosen license]
