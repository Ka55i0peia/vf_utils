from bulk_edit import FinishEstimator, log
from random import randrange
import time
import logging
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    log.load_config()
    elements = 100
    progress = FinishEstimator(elements, windowSize=7)

    for i in range(elements):
        if i < 10:
            waittime = randrange(1, 5)
            time.sleep(waittime)
        else:
            time.sleep(1)

        progress.tick()
        progress.log_progress(logger)
