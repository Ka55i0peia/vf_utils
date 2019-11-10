import tasks
import os
import logging
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    try:
        login = tasks.LoginToVf(headlessMode=False)

        login.execute()
        driver = login.webdriver

        changeUser = tasks.ChangeUserStatus(driver, uid="249109", statusName="Ordentliches Mitglied")
        changeUser.execute()
    except Exception as ex:
        logger.error(ex)
        logger.debug("Trace:\n", exc_info=ex)
