import tasks
from task_executor import TaskExecutor
from logconfig import load_log_config
import atexit
import os
import logging
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    load_log_config()
    try:
        login = tasks.LoginToVf(headlessMode=False)

        login.execute()
        driver = login.webdriver

        # prepare task list
        taskList = []
        with open("input/gaeste_2019.txt", "r") as f:
            line = f.readline()
            while line:
                t = tasks.ChangeUserStatus(driver, uid=int(line), statusName="Gastverein Zugangsberechtigung abgelaufen")
                taskList.append(t)
                line = f.readline()

        batchProcess = TaskExecutor()
        # log process results in every state (even it's interrupted by user or exception)
        atexit.register(batchProcess.log_summary, logger)
        # executes all tasks
        batchProcess.execute(taskList)

    except KeyboardInterrupt as ex:
        logger.info("User interrupted")

    except Exception as ex:
        logger.error(ex)
        logger.debug("Trace:\n", exc_info=ex)
