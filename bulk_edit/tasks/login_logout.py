from bulk_edit.tasks import Task
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from typing import List, Tuple
from getpass import getpass
import logging
logger = logging.getLogger(__name__)


class LoginToVf(Task):

    def __init__(self, driver: webdriver, credentialFile: str = '', user: str = ''):
        self.driver = driver
        self.credentialFile = credentialFile
        self.user = user

    @classmethod
    def parameters(cls) -> List[str]:
        # TODO add some more info about parameter like type and description
        return ['credentialFile']

    def ident(self) -> str:
        return f"VF Login with credentialFile '{self.credentialFile}'"

    # NOTE candidate for global utility
    @staticmethod
    def get_user_and_passwd_from_file(fileName: str) -> Tuple[str, str]:
        user = None
        pwd = None
        with open(fileName, 'r') as f:
            # first line:
            user = f.readline()
            # second line:
            pwd = f.readline()

        # error check
        if len(user) == 0 or len(pwd) == 0:
            raise Exception(f"Crendential file '{fileName}' must contain a user "
                            "in the first line and password in the second line")

        return (user, pwd)

    @staticmethod
    def get_user_and_pwd_from_cli(user: str = '') -> Tuple[str, str]:
        print('Please enter user password to login to vereinflieger.de')
        if user == '':
            user = input('user: ')
        pwd = getpass('password: ')
        return (user, pwd)

    def execute(self) -> bool:
        self.driver.get("https://vereinsflieger.de/")

        # check if we are already logged in ..
        try:
            self.driver.find_element_by_link_text("Mein Profil")
            return True
        except NoSuchElementException:
            # no, we aren't logged in already
            pass

        # get credentials
        if self.credentialFile is not None:
            try:
                (user, pwd) = type(self).get_user_and_passwd_from_file(self.credentialFile)
            except Exception as ex:
                logger.error(f"Reading credential file '{self.credentialFile}' failed.")
                logger.debug(ex, exc_info=ex)
                # fallback
                (user, pwd) = type(self).get_user_and_pwd_from_cli(self.user)
        else:
            (user, pwd) = type(self).get_user_and_pwd_from_cli(self.user)

        # login
        self.driver.find_element_by_name("user").send_keys(user)
        self.driver.find_element_by_name("pwinput").send_keys(pwd)
        self.driver.find_element_by_name("submit").click()

        return True
