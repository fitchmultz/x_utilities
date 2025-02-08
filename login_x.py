# <ai_context>Module for handling login and browser session for X</ai_context>
import json
import logging

from playwright.sync_api import sync_playwright

from config import (
    COOKIES_FILENAME,
    HEADLESS,
    HOME_URL,
    MANUAL_LOGIN_TIMEOUT,
    PAGE_LOAD_TIMEOUT,
    PROFILE_URL,
)

logger = logging.getLogger(__name__)

def setup_browser():
    """Initialize and return browser context with cookies if available"""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=HEADLESS)
    context = browser.new_context()

    # Load saved cookies if available
    try:
        with open(COOKIES_FILENAME, "r") as f:
            cookies = json.load(f)
            context.add_cookies(cookies)
            logger.info("Cookies loaded successfully.")
    except Exception as e:
        logger.warning("No cookies found or error loading cookies: %s", e)
        logger.info("You must log in manually to generate cookies.")

    return playwright, browser, context


def handle_login(page, context):
    """Handle login process and save cookies if needed"""
    if "login" in page.url.lower():
        logger.info("Not logged in. Please log in manually in the opened browser window.")
        page.wait_for_timeout(MANUAL_LOGIN_TIMEOUT)

        # Save cookies after successful login
        cookies = context.cookies()
        with open(COOKIES_FILENAME, "w") as f:
            json.dump(cookies, f)
            logger.info("Cookies saved to %s", COOKIES_FILENAME)


def navigate_to_profile(page):
    """Navigate to the user's profile page"""
    page.goto(PROFILE_URL)
    page.wait_for_timeout(PAGE_LOAD_TIMEOUT)
    logger.info("Successfully navigated to your profile: %s", page.url)


def ensure_logged_in():
    """Main function to ensure user is logged in and return browser session"""
    playwright, browser, context = setup_browser()
    page = context.new_page()

    # Navigate to homepage
    page.goto(HOME_URL)
    page.wait_for_timeout(PAGE_LOAD_TIMEOUT)

    # Handle login if needed
    handle_login(page, context)

    return playwright, browser, context, page


if __name__ == "__main__":
    # When run directly, just handle login
    playwright, browser, context, page = ensure_logged_in()
    try:
        navigate_to_profile(page)
    finally:
        browser.close()
        playwright.stop()