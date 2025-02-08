# <ai_context>Main entry point for X (Twitter) Utilities</ai_context>
import os
import logging
import logger_setup  # Ensure logging is configured

from config import CONFIG_DIR, FORCE_LAYOUT_DISCOVERY, LAYOUT_CONFIG
from login_x import ensure_logged_in, navigate_to_profile

logger = logging.getLogger(__name__)

def needs_layout_discovery():
    """Check if we need to discover the X layout"""
    return FORCE_LAYOUT_DISCOVERY or not os.path.exists(LAYOUT_CONFIG)


def main():
    logger.info("Starting main execution.")
    # Create config directory if it doesn't exist
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # Initialize browser and ensure logged in
    playwright, browser, context, page = ensure_logged_in()

    try:
        # Navigate to profile
        navigate_to_profile(page)

        # Check if we need to discover the layout
        if needs_layout_discovery():
            from discover import discover_layout
            discover_layout(page)
    finally:
        browser.close()
        playwright.stop()
        logger.info("Browser closed and playwright stopped.")


if __name__ == "__main__":
    main()