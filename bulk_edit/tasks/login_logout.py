from bulk_edit.tasks import Task
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException


class LoginToVf(Task):

    def __init__(self, headlessMode: bool, credentialFile: str = "vf_login_credentials.txt"):
        self.headlessMode = False
        self._webdriver = None
        self.credentialFile = credentialFile

    def ident(self) -> str:
        return f"VF Login with credentialFile '{self.credentialFile}'"

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
