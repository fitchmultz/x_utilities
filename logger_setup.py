# <ai_context>Logger configuration for the entire project</ai_context>
import logging

logging.basicConfig(
    level=logging.INFO,  # Set default logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)