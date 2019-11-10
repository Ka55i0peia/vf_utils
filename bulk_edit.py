import tasks
import os
import logging
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    login = tasks.LoginToVf(headlessMode=False)

    login.execute()
    driver = login.webdriver

    changeUser = tasks.ChangeUserProperty(driver, uid="249109", flightClub="Bünde")
    changeUser.execute()
