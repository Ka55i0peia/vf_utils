from bulk_edit import tasks, log, TaskExecutor
from bulk_edit.tasks.members import community as community_task
import atexit
import logging
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    log.load_config()
    try:
        login = tasks.LoginToVf(headlessMode=False)

        login.execute()
        driver = login.webdriver

        # prepare task list
        # TODO provide a CLI!
        # TODO provide the line wise reading as task
        # TODO ui suggestion: let the user define the chain in a simple txt file
        taskList = []
        with open("input/gaeste_2019.txt", "r") as f:
            line = f.readline()
            while line:
                # prepare task
                taskParameter = {
                    "webdriver": driver,
                    "uid": int(line),
                    "statusName": "Gastverein Zugangsberechtigung abgelaufen"
                }
                task = community_task.ChangeUserStatus
                taskList.append(task(**taskParameter))
                # makes this loop a for each line
                line = f.readline()

        batchProcess = TaskExecutor()
        # log process results in every state (even it's interrupted by user or exception)
        atexit.register(batchProcess.log_summary, logger)
        # executes all tasks
        batchProcess.execute(taskList)

    except KeyboardInterrupt:
        logger.info("User interrupted")

    except Exception as ex:
        logger.error(ex)
        logger.debug("Trace:\n", exc_info=ex)
