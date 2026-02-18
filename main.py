import logging
from pathlib import Path
import sys

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme
from rich.traceback import install
import uvicorn

from app.core.config import settings
from app.database.vector_db import create_qdrant_collection

sys.path.extend([str(Path(__file__).parent)])


def configure_logger():
    install()

    custom_theme = Theme(
        {
            "logging.level.debug": "cyan",
            "logging.level.info": "green",
            "logging.level.warning": "yellow",
            "logging.level.error": "bold red",
            "logging.level.critical": "bold white on red",
        }
    )

    console = Console(theme=custom_theme)

    handler = RichHandler(console=console, rich_tracebacks=True, markup=True)

    logging.basicConfig(
        level=logging.INFO, format="%(message)s", handlers=[handler], force=True
    )


configure_logger()

if __name__ == "__main__":
    create_qdrant_collection()
    uvicorn.run(
        app="app.server:app",
        host=settings.HOST,
        port=settings.PORT,
        log_config=None,
    )
