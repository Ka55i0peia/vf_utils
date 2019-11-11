import tasks
from task_executor import TaskExecutor
import os
import logging
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    try:
        login = tasks.LoginToVf(headlessMode=False)

        login.execute()
        driver = login.webdriver

        # prepare task list
        taskList = []
        with open("input/gaeste_2019.txt", "r") as f:
            line = f.readline()
            while line:
                t = tasks.ChangeUserStatus(driver, uid=line, statusName="Gastverin Zugangsberechtigung abgelaufen")
                taskList.append(t)
                line = f.readline()

        batchProcess = TaskExecutor()
        batchProcess.execute(tasks)
    except Exception as ex:
        logger.error(ex)
        logger.debug("Trace:\n", exc_info=ex)
