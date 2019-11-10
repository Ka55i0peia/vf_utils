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

    def __init__(self, headlessMode: bool, user: str, passwd: str):
        self.headlessMode = False
        self.user = user
        self.passwd = passwd
        self._webdriver = None

    @property
    def webdriver(self) -> webdriver:
        if self._webdriver is None:
            raise Exception("Execute LoginToVf task first!")

        return self._webdriver

    @property
    def permutable(self) -> bool:
        return False

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
            driver.find_element_by_name("user").send_keys(self.user)
            driver.find_element_by_name("pwinput").send_keys(self.passwd)
            driver.find_element_by_name("submit").click()

            return True
        except Exception as ex:
            logger.error(ex)
            logger.debug("Trace:\n", exc_info=ex)
            return False


class ChangeUserProperty(TaskBase):

    def __init__(self, webdriver: webdriver, uid: str, flightClub: str, customPropertyNo: int = 1):
        '''
        `ui` user to edit
        `flightClub` custom property value to set (by string representation)
        '''
        self.webdriver = webdriver
        self.uid = uid
        self.flightClub = flightClub
        # this is the html name property for the custom property drop down (on editfunctions.php)
        self.customPropertySelector = f"suc_prop_512_{customPropertyNo}"

    def execute(self) -> bool:
        driver = self.webdriver
        # TODO move this common exception handling to an annotation (follow aspect oriented programming)
        try:
            driver.get(f"https://vereinsflieger.de/member/community/editfunctions.php?uid={self.uid}")

            # get dropdown element and select club
            selector = Select(driver.find_element_by_name(self.customPropertySelector))
            selector.select_by_visible_text(self.flightClub)

            # hit the save button
            driver.find_element_by_name("submit_").click()

            # TODO implement a checker for valid input (may make use of JS function: checkMandatory())
            return True
        except Exception as ex:
            logger.error(ex)
            logger.debug("Trace:\n", exc_info=ex)
            return False
