# <ai_context>Module for interacting with Google Gemini API</ai_context>
import json
import logging
import os

import google.generativeai as genai

logger = logging.getLogger(__name__)


def analyze_layout_with_gemini(layout_file_path):
    """Send layout JSON to Google Gemini and return structured analysis."""
    logger.info("Reading layout data from %s", layout_file_path)
    with open(layout_file_path, "r") as f:
        layout_data = f.read()

    # Configure Gemini
    logger.debug("Configuring Gemini API with provided key")
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Setup the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }
    logger.debug("Initializing Gemini model with configuration")
    model = genai.GenerativeModel(
        model_name="gemini-2.0-pro-exp-02-05",
        generation_config=generation_config,
        system_instruction=(
            'Examine the contents of "layout.json", which contains a list of HTML elements and their attributes. '
            'Identify key interactive components on the webpage that are used for essential functions such as composing tweets, '
            'checking notifications, navigating the profile, viewing messages, etc. For each component, determine the CSS selector, '
            'its type (e.g., button, link, div), and the primary action it is associated with (e.g., "compose tweet", "check notifications"). '
            'Return the result as a JSON object structured as follows: {"element_selector_mapping": { "element_name": {"selector": "CSS_SELECTOR", "type": "element_type", "action": "function_description"} } }. '
            'Ensure that the keys in the mapping are alphabetically ordered.'
        ),
    )

    # Start chat session
    logger.debug("Starting chat session with layout data")
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [f"```json\n{layout_data}\n```"],
            }
        ]
    )

    # Ask for structured JSON
    logger.info("Requesting structured JSON analysis from Gemini")
    response = chat_session.send_message(
        "Return structured JSON with a mapping of element names to their CSS selectors, type, and associated functionality. "
        "The JSON should have a top-level key 'element_selector_mapping'. For each element, include 'selector', 'type', and 'action' describing its function (e.g., composing tweets, checking notifications, navigating to profile, viewing messages). "
        "Ensure the keys are sorted alphabetically."
    )

    # Try to parse the response as JSON
    try:
        data = json.loads(response.text)
        logger.info("Successfully parsed Gemini response as JSON")
    except json.JSONDecodeError:
        logger.warning(
            "Failed to parse Gemini response as JSON, returning raw response"
        )
        data = {"raw_response": response.text}

    return data