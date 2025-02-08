# <ai_context>Module for discovering and documenting X's layout</ai_context>
import glob
import json
import logging
import os
from datetime import datetime
from time import sleep

from config import (
    LAYOUT_CONFIG,
    MEDIA_TIMEOUT_MS,
    SCREENSHOTS_DIR,
    SCROLL_COUNT,
    SCROLL_WAIT_MS,
    CONFIG_DIR
)
from gemini_api import analyze_layout_with_gemini

logger = logging.getLogger(__name__)


def wait_for_page_load(page):
    """Wait for the page to be fully loaded and hydrated"""
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")

    selectors = [
        "article",
        "[data-testid='primaryColumn']",
        "[role='button']",
        "img",
        "video",
        "[data-testid='tweetPhoto']",
    ]

    for selector in selectors:
        try:
            page.wait_for_selector(selector, timeout=MEDIA_TIMEOUT_MS)
        except Exception:
            logger.warning(
                "Warning: Could not find element '%s' after waiting", selector
            )

    try:
        page.evaluate(
            """() => {
            return new Promise((resolve, reject) => {
                const mediaPromises = [];

                // Wait for images
                document.querySelectorAll('img').forEach(img => {
                    if (!img.complete) {
                        mediaPromises.push(new Promise(resolve => {
                            img.onload = resolve;
                            img.onerror = resolve;
                        }));
                    }
                });

                // Wait for videos
                document.querySelectorAll('video').forEach(video => {
                    if (video.readyState < 2) {
                        mediaPromises.push(new Promise(resolve => {
                            video.onloadeddata = resolve;
                            video.onerror = resolve;
                        }));
                    }
                });

                if (mediaPromises.length === 0) {
                    resolve();
                } else {
                    Promise.all(mediaPromises).then(resolve).catch(reject);
                }
            });
        }"""
        )
    except Exception as e:
        logger.warning(
            "Warning: Some media elements did not load completely: %s", str(e)
        )


def cleanup_old_screenshots():
    """Remove all existing screenshots"""
    if os.path.exists(SCREENSHOTS_DIR):
        for file in glob.glob(os.path.join(SCREENSHOTS_DIR, "layout_discovery_*.png")):
            try:
                os.remove(file)
                logger.info("Removed old screenshot: %s", file)
            except Exception as e:
                logger.warning(
                    "Warning: Could not remove old screenshot %s: %s", file, str(e)
                )


def capture_screenshot(page):
    """Capture a screenshot of the current page"""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    cleanup_old_screenshots()

    for _ in range(SCROLL_COUNT):
        page.evaluate("window.scrollBy(0, window.innerHeight)")
        page.wait_for_timeout(SCROLL_WAIT_MS)
        try:
            wait_for_page_load(page)
        except Exception:
            logger.warning("Warning: Some media elements did not load after scrolling")

    page.wait_for_timeout(2000)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"layout_discovery_{timestamp}.png")
    page.screenshot(path=screenshot_path, full_page=True)
    logger.info("Screenshot saved to %s", screenshot_path)
    return screenshot_path


def analyze_page_structure(page):
    """Analyze the page structure and identify key elements"""
    elements_to_find = {
        "tweet": {
            "container": None,
            "text": None,
            "timestamp": None,
            "metrics": None,
            "media": None,
        },
        "profile": {
            "name": None,
            "bio": None,
            "following_count": None,
            "followers_count": None,
        },
        "navigation": {"home": None, "explore": None, "messages": None},
    }

    elements = page.evaluate(
        """() => {
        function hasMeaningfulContent(el) {
            const text = el.textContent.trim();
            return text.length > 0 ||
                   el.querySelector('img') !== null ||
                   el.getAttribute('role') === 'button' ||
                   el.getAttribute('aria-label') !== null;
        }

        const relevantTags = ['article', 'div', 'span', 'a', 'button', 'img'];
        const elems = document.querySelectorAll(relevantTags.join(','));

        return Array.from(elems)
            .filter(el => hasMeaningfulContent(el))
            .map(el => ({
                tag: el.tagName.toLowerCase(),
                classes: Array.from(el.classList)
                    .filter(cls => !cls.startsWith('r-')),
                role: el.getAttribute('role'),
                ariaLabel: el.getAttribute('aria-label'),
                text: el.textContent.trim().slice(0, 100),
                hasImage: el.tagName === 'IMG' || el.querySelector('img') !== null,
                href: el.tagName === 'A' ? el.getAttribute('href') : null
            }));
    }"""
    )

    layout_data = {
        "timestamp": datetime.now().isoformat(),
        "url": page.url,
        "elements": elements,
        "identified_components": elements_to_find,
    }

    return layout_data


def discover_layout(page):
    """Main function to discover and document X's layout"""
    logger.info("Starting layout discovery...")
    wait_for_page_load(page)
    screenshot_path = capture_screenshot(page)
    layout_data = analyze_page_structure(page)
    layout_data["screenshot_path"] = screenshot_path

    with open(LAYOUT_CONFIG, "w") as f:
        json.dump(layout_data, f, indent=2)
        logger.info("Layout configuration saved to %s", LAYOUT_CONFIG)

    # Send layout.json to Gemini and save analysis
    gemini_data = analyze_layout_with_gemini(LAYOUT_CONFIG)
    layout_selectors_path = os.path.join(CONFIG_DIR, "layout_selectors.json")
    with open(layout_selectors_path, "w") as fs:
        json.dump(gemini_data, fs, indent=2)
    logger.info("Gemini analysis saved to %s", layout_selectors_path)

    logger.info("Layout discovery completed!")
    return layout_data