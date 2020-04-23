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
        # fallback
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "brief": {
                    "class": "logging.Formatter",
                    "format": "%(asctime)s %(levelname)-8s %(message)s",
                    "datefmt": "%H:%M:%S"
                },
                "detailed": {
                    "class": "logging.Formatter",
                    "format": "%(asctime)s %(name)-15s %(levelname)-8s %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "brief"
                },
                "file": {
                    "class": "logging.FileHandler",
                    "filename": "full.log",
                    "mode": "w",
                    "level": "DEBUG",
                    "formatter": "detailed"
                }
            },
            "loggers": {
                "urllib3": {
                    "level": "WARN"
                },
                "selenium": {
                    "level": "WARN"
                }
            },
            "root": {
                "handlers": ["console", "file"],
                "level": "DEBUG"
            }
        }
        logging.config.dictConfig(config)

        # write a config file
        with open("logconfig.json", "w") as f:
            config = json.dump(config, f)
            logger.info("log config file was written")
