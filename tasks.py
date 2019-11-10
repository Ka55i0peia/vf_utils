import abc
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from typing import Optional
import logging
logger = logging.getLogger(__name__)

class TaskBase:

    @abc.abstractmethod
    def execute(self) -> bool:
        pass

    @property
    def permutable(self) -> bool:
        return True


class LoginToVf(TaskBase):

    def __init__(self, headlessMode: bool, credentialFile: str = "vf_login_credentials.txt"):
        self.headlessMode = False
        self._webdriver = None
        self.credentialFile = credentialFile

    @property
    def webdriver(self) -> webdriver:
        if self._webdriver is None:
            raise Exception("Execute LoginToVf task first!")

        return self._webdriver

    @property
    def permutable(self) -> bool:
        return False

    # NOTE candidate for global utility
    @staticmethod
    def get_user_and_passwd_from_file(fileName: str) -> (str, str):
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

    def execute(self) -> bool:
        profile = webdriver.FirefoxProfile()
        options = Options()
        # this line starts FF in headless mode
        options.headless = self.headlessMode

        driver = webdriver.Firefox(firefox_profile=profile, options=options)
        self._webdriver = driver
        # TODO move this common exception handling to an annotation (follow aspect oriented programming)
        try:
            driver.get("https://vereinsflieger.de/")

            # check if we are already logged in ..
            try:
                driver.find_element_by_link_text("Mein Profil")
                return True
            except NoSuchElementException:
                # no, we aren't logged in already
                pass

            # login
            (user, pwd) = type(self).get_user_and_passwd_from_file(self.credentialFile)
            driver.find_element_by_name("user").send_keys(user)
            driver.find_element_by_name("pwinput").send_keys(pwd)
            driver.find_element_by_name("submit").click()

            return True
        except Exception as ex:
            logger.error(ex)
            logger.debug("Trace:\n", exc_info=ex)
            return False


class DropdownChangeBase(TaskBase):

    def __init__(self, **kwargs):
        self.webdriver = kwargs["webdriver"]
        self.value = kwargs["value"]
        # this is the html name property for the custom property drop down (on editfunctions.php)
        self.htmlSelector = kwargs["htmlSelector"]
        self.changeUrl = kwargs["changeUrl"]
        if "saveButtonName" not in kwargs:
            self.saveButtonName = "submit_"
        else:
            self.saveButtonName = kwargs["saveButtonName"]

    def execute(self) -> bool:
        driver = self.webdriver
        # TODO move this common exception handling to an annotation (follow aspect oriented programming)
        try:
            driver.get(self.changeUrl)

            # get dropdown element and select club
            selector = Select(driver.find_element_by_name(self.htmlSelector))
            selector.select_by_visible_text(self.value)

            # hit the save button
            driver.find_element_by_name(self.saveButtonName).click()

            # TODO implement a checker for valid input (may make use of JS function: checkMandatory())
            return True
        except Exception as ex:
            logger.error(ex)
            logger.debug("Trace:\n", exc_info=ex)
            return False


class ChangeUserProperty(DropdownChangeBase):

    def __init__(self, webdriver: webdriver, uid: str, flightClub: str, customPropertyNo: int = 1):
        '''
        `ui` user to edit
        `flightClub` custom property value to set (by string representation)
        '''
        super().__init__(webdriver=webdriver,
                         changeUrl=f"https://vereinsflieger.de/member/community/editfunctions.php?uid={uid}",
                         value=flightClub,
                         htmlSelector=f"suc_prop_512_{customPropertyNo}")

