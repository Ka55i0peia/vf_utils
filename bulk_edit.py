import tasks
import os
import logging
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    login = tasks.LoginToVf(headlessMode=False)

    login.execute()
    driver = login.webdriver

    changeUser = tasks.ChangeUserStatus(driver, uid="249109", statusName="Ordentliches Mitglied")
    changeUser.execute()
