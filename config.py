import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Browser configuration
HEADLESS = False  # Run browser in visible mode

# URLs and user info
HOME_URL = "https://x.com"
PROFILE_USERNAME = os.getenv(
    "PROFILE_USERNAME", "yourusername"
)  # Get from .env, fallback to default
PROFILE_URL = f"https://x.com/{PROFILE_USERNAME}"

# File paths
CONFIG_DIR = "config"
COOKIES_FILENAME = "cookies.json"
LAYOUT_CONFIG = os.path.join(CONFIG_DIR, "layout.json")
SCREENSHOTS_DIR = os.path.join(CONFIG_DIR, "screenshots")

# Discovery settings
FORCE_LAYOUT_DISCOVERY = True  # Set to True to run discovery every time
SCROLL_COUNT = 5  # Number of times to scroll for content loading
SCROLL_WAIT_MS = 1100  # Time to wait after each scroll in milliseconds
MEDIA_TIMEOUT_MS = 5000  # Time to wait for media elements to load

# Timeouts
PAGE_LOAD_TIMEOUT = 5000  # Milliseconds to wait for page load
MANUAL_LOGIN_TIMEOUT = 60000  # Milliseconds to wait for manual login
