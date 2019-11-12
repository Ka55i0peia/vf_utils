import json
import logging
import logging.config
logger = logging.getLogger(__name__)


def load_config():
    try:
        with open("logconfig.json", "r") as f:
            config = json.load(f)
            logging.config.dictConfig(config)
            logger.debug("Log config loaded successfully")
    except Exception as ex:
        logger.error(f"Loading log config failed with message: {ex}")
