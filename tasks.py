import abc
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from typing import Optional
import logging
logger = logging.getLogger(__name__)


class Task:

    @abc.abstractmethod
    def execute(self) -> bool:
        pass


class LoginToVf(Task):

    def __init__(self, headlessMode: bool, credentialFile: str = "vf_login_credentials.txt"):
        self.headlessMode = False
        self._webdriver = None
        self.credentialFile = credentialFile

    @property
    def webdriver(self) -> webdriver:
        if self._webdriver is None:
            raise Exception("Execute LoginToVf task first!")

        return self._webdriver

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

class ComboboxChange(Task):

    def __init__(self, webdriver: webdriver, changeUrl: str, cmbxHtmlName: str,
                 cmbxTextValue: str):
        self.webdriver = webdriver
        self.cmbxTextValue = cmbxTextValue
        # this is the html name property for the custom property drop down (on editfunctions.php)
        self.cmbxHtmlName = cmbxHtmlName
        self.changeUrl = changeUrl

    def execute(self) -> bool:
        driver = self.webdriver

        # open webpage
        driver.get(self.changeUrl)

        # get dropdown element and select value
        combobox = driver.find_element_by_name(self.cmbxHtmlName)
        selector = Select(combobox)
        selector.select_by_visible_text(self.cmbxTextValue)

        # hit the submit method on element. (This lets silenumn walk up the DOM tree 
        # to the <form> tag and submit it.)
        combobox.submit()

        # TODO implement a checker for valid input (may make use of JS function: checkMandatory())
        return True

class ChangeUserClubProperty(ComboboxChange):

    def __init__(self, webdriver: webdriver, uid: str, flightClub: str, customPropertyNo: int = 1):
        '''
        `ui` user to edit
        `flightClub` custom property value to set (by string representation)
        '''
        url = f"https://vereinsflieger.de/member/community/editfunctions.php?uid={uid}"
        super().__init__(webdriver=webdriver,
                         changeUrl=url,
                         cmbxTextValue=flightClub,
                         cmbxHtmlName=f"suc_prop_512_{customPropertyNo}")


class ChangeUserStatus(ComboboxChange):

    def __init__(self, webdriver: webdriver, uid: str, statusName: str):
        '''
        `ui` user to edit
        `statusName` status to be set
        '''
        url = f"https://vereinsflieger.de/member/community/editcommunity.php?uid={uid}"
        super().__init__(webdriver=webdriver,
                         changeUrl=url,
                         cmbxTextValue=statusName,
                         cmbxHtmlName=f"frm_msid")

