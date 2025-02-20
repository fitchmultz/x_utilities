# X (Twitter) Utilities

A Python-based toolkit for interacting with X (Twitter) using browser automation and AI-driven analysis. This project leverages Playwright for seamless navigation and interaction with X, and integrates Google’s Gemini API to intelligently analyze page layouts. It’s designed for developers, researchers, and data enthusiasts looking to explore X’s structure and content programmatically.

## Project Overview

X Utilities automates interactions with X, including login, profile navigation, and layout discovery. It captures screenshots, extracts structured data about page elements, and uses AI to identify key interactive components (e.g., buttons for composing tweets or checking notifications). The output is saved as JSON files for further use, making it a versatile tool for web scraping, research, or automation tasks.

## How It Works

1. **Login and Session Management** (`login_x.py`):

   - Uses Playwright to launch a Chromium browser (headless or visible).
   - Loads saved cookies or prompts for manual login, persisting cookies for future sessions.

2. **Profile Navigation** (`main.py`):

   - Navigates to a specified X profile (configurable via `PROFILE_USERNAME`).

3. **Layout Discovery** (`discover.py`):

   - Scrolls through the page, waits for content (e.g., tweets, images, videos) to load.
   - Captures full-page screenshots and saves them with timestamps.
   - Analyzes the DOM to extract elements with meaningful content (e.g., articles, buttons, media).
   - Saves raw layout data to `layout.json`.

4. **AI-Powered Analysis** (`gemini_api.py`):

   - Sends `layout.json` to the Google Gemini API.
   - Receives a structured JSON response mapping elements to CSS selectors, types, and actions (e.g., “compose tweet”).
   - Saves the analysis to `layout_selectors.json`.

5. **Configuration** (`config.py`):
   - Centralizes settings like timeouts, scroll counts, and file paths, loaded from a `.env` file.

The workflow is orchestrated by `main.py`, which ensures login, navigation, and layout discovery run smoothly.

## AI and Machine Learning Usage

This project integrates **Google’s Gemini API**, a generative AI model, to analyze X’s dynamic page layouts. Here’s how it’s used:

- **Input**: The API receives `layout.json`, containing raw HTML element data (tags, classes, text, etc.) extracted by Playwright.
- **Task**: Gemini identifies key interactive components (e.g., tweet compose button, navigation links) and determines their purpose based on attributes and context.
- **Output**: A structured JSON (`layout_selectors.json`) with CSS selectors, element types, and actions, sorted alphabetically for consistency.
- **Why AI?**: X’s frequent UI updates make static scraping unreliable. Gemini’s natural language understanding and pattern recognition adapt to these changes, providing robust, automated selector generation.

This AI-driven approach reduces manual effort and enhances the tool’s resilience to X’s evolving structure.

## Installation

### Prerequisites

- Python 3.11+
- Playwright and Chromium browser
- Google Gemini API key (set in `.env`)

### Steps

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd x_utilities
   ```

2. Set up a virtual environment:

   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
   ```

4. Configure environment:
   - Copy `.env.example` to `.env` and add your `GEMINI_API_KEY` and `PROFILE_USERNAME`.
   - Optionally, copy `cookies.json.example` to `cookies.json` and update with your X auth token (see “How to Get Your Auth Cookie”).

### How to Get Your Auth Cookie

1. Log into X in Chrome.
2. Open Developer Tools (F12) > Application > Cookies > `x.com`.
3. Use the [Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/iphcomljdfghbkdcfndaijbokpgddeno) extension to export cookies as `cookies.json`.

## Usage

Run the main script:

```bash
python main.py
```

### What Happens

1. Creates a `config/` directory for outputs.
2. Logs in using cookies or prompts for manual login.
3. Navigates to the specified profile.
4. Performs layout discovery (if forced or `layout.json` is missing), saving screenshots and JSON data.

### Outputs

- `config/layout.json`: Raw page structure.
- `config/layout_selectors.json`: AI-analyzed selectors.
- `config/screenshots/`: Timestamped PNGs.

## Potential Use Cases

Beyond its current functionality, X Utilities can be extended for:

1. **Social Media Research**:

   - Analyze X profile layouts to study UI/UX trends across platforms.
   - Track how X’s design evolves over time with periodic snapshots.

2. **Content Scraping**:

   - Extract tweets, media, or user metrics for sentiment analysis or data journalism.
   - Build datasets for training ML models (e.g., tweet classification).

3. **Automation Bots**:

   - Automate posting, liking, or following based on AI-identified selectors.
   - Monitor notifications or messages in real-time.

4. **Competitive Analysis**:

   - Compare X’s layout with other social platforms (e.g., Threads, Mastodon) using the same AI pipeline.

5. **Accessibility Auditing**:

   - Use Gemini to flag missing ARIA labels or inaccessible elements in X’s UI.

6. **Educational Tools**:
   - Teach web scraping, browser automation, or AI integration with a practical, real-world example.

## Project Structure

```txt
x_utilities/
├── config/                 # Output directory
│   ├── layout.json        # Raw layout data
│   ├── layout_selectors.json # AI-analyzed selectors
│   └── screenshots/       # Captured screenshots
├── x_utilities/
│   ├── config.py          # Settings and constants
│   ├── discover.py        # Layout discovery logic
│   ├── gemini_api.py      # AI analysis with Gemini
│   ├── logger_setup.py    # Logging configuration
│   ├── login_x.py         # Browser and login handling
│   ├── main.py            # Program entry point
│   ├── README.md          # This file
│   └── requirements.txt   # Dependencies
├── .env.example           # Environment template
└── cookies.json.example   # Cookie template
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

Suggestions: Add new scraping features, improve AI prompts, or enhance error handling.
