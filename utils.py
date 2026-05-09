from datetime import datetime
from pathlib import Path
from loguru import logger
from src.config import LOG_DIR

LOG_DIR.mkdir(exist_ok=True)

logger.add(
    LOG_DIR / "automation.log",
    rotation="1 MB",
    retention="10 days",
    level="INFO"
)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_folder(path: Path):
    path.mkdir(parents=True, exist_ok=True)