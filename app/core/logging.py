from logging import Logger
from app.core.config import settings

logger = Logger(name=settings.app_name, level=settings.log_level)
