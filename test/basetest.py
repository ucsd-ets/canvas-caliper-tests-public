import pytest
import time
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


@pytest.mark.usefixtures("driver_init")
class BaseTest:
    # def __init__(self):
    #   pass
    SECONDS_WAIT = 10
    SSO_USERNAME = "testacct111"

    BASE_URL = "https://canvas.ucsd.edu"

    def login_sso(self):
        SSO_PASS = os.getenv("CANVAS_SSO_PASS")

        # 3 | click | linkText=Sign in |  | Click Sign In button on Landing Page
        self.driver.find_element(By.LINK_TEXT, "Sign in").click()
        # 4 | click | css=.login-saml-default |  | Click SSO Sign In Button on Log In Page

        # pj added for sauce
        WebDriverWait(self.driver, self.SECONDS_WAIT).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, ".login-saml-default")
            )
        )

        self.driver.find_element(By.CSS_SELECTOR, ".login-saml-default").click()
        # 5 | type | id=ssousername | testacct111 | Enter Username
        # pj added for sauce
        WebDriverWait(self.driver, self.SECONDS_WAIT).until(
            expected_conditions.presence_of_element_located((By.ID, "ssousername"))
        )

        self.driver.find_element(By.ID, "ssousername").send_keys(self.SSO_USERNAME)
        # 6 | click | id=ssopassword |  | Click Password Field
        self.driver.find_element(By.ID, "ssopassword").click()
        # 7 | type | id=ssopassword | LearnXedX1 | Enter Password
        self.driver.find_element(By.ID, "ssopassword").send_keys(SSO_PASS)
        # 8 | click | name=_eventId_proceed |  | Click Sign in Button
        self.driver.find_element(By.NAME, "_eventId_proceed").click()
        # 9 | waitForElementVisible | id=footerLogo | 30000 |
        WebDriverWait(self.driver, self.SECONDS_WAIT).until(
            expected_conditions.visibility_of_element_located((By.ID, "footerLogo"))
        )
        # 10 | verifyElementPresent | id=my-courses |  | Verify Courses Panel Loaded
        elements = self.driver.find_elements(By.ID, "my-courses")
        assert len(elements) > 0

    def wait_for_ajax(self, driver):
        wait = WebDriverWait(driver, self.SECONDS_WAIT)

        wait.until(lambda driver: driver.execute_script("return jQuery.active") == 0)

        # https://github.com/seleniumhq/selenium/issues/2388
        # edge webdriver does not wait for readyState=complete
        wait.until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )

    def wait_for_page_load(self, driver):
        self.wait_for_ajax(driver)

    def move_to_element(self, element):
        try:
            if os.environ["device"] == "desktop" and (
                os.environ["browser"] == "chrome" or os.environ["browser"] == "edge"
            ):
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(element, 0, 0).click().perform()
        except Exception:
            raise

    def scroll_to_bottom(self):
        try:

            SCROLL_PAUSE_TIME = 0.5

            # Get scroll height
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

            while True:
                # Scroll down to bottom
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if new_height == last_height:
                    break
                last_height = new_height

        except Exception:
            raise


class DesktopBaseTest(BaseTest):
    def login_non_sso(self):
        try:
            self.driver.get(self.BASE_URL)
            super().login_non_sso()

        except Exception:
            raise

    def login_sso(self):
        try:
            self.driver.get(self.BASE_URL)

            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located((By.ID, "main"))
            )

            # 2 | verifyElementPresent | id=main |  | Verify Welcome Message Loads
            elements = self.driver.find_elements(By.ID, "main")
            assert len(elements) > 0

            # 2 | setWindowSize | 1247x573 |  | Set Window Size, avoid hamburger menu
            self.driver.set_window_size(1247, 573)

            super().login_sso()

        except Exception:
            raise


class MobileBaseTest(BaseTest):
    def login_non_sso(self):
        try:
            NON_SSO_PASS = os.getenv("CANVAS_NON_SSO_PASS")
            self.driver.get(self.BASE_URL)
            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, "hamburger-menu")
                )
            ).click()
            # super().login_non_sso()

            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located(
                    (By.LINK_TEXT, "Sign in")
                )
            )

            # 2 | click | linkText=Sign in |  |
            self.driver.find_element(By.LINK_TEXT, "Sign in").click()

            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located((By.ID, "login-email"))
            )

            element = self.driver.find_element(By.ID, "login-email")

            # 3 | click | id=login-email |  |
            self.driver.find_element(By.ID, "login-email").click()
            # 4 | type | id=login-email | learnxqa+1218191@gmail.com |
            self.driver.find_element(By.ID, "login-email").send_keys(self.NON_SSO_EMAIL)
            # 5 | type | id=login-password | OpenedX!2019 |
            self.driver.find_element(By.ID, "login-password").send_keys(NON_SSO_PASS)
            # 6 | click | css=.action-update
            # xpath = "/html/body/div[2]/div[3]/div/main/div/div/section[1]/div/form/button"
            # new chrome requires we manually move to (nearby) element first
            element = self.driver.find_element(
                By.XPATH, "/html/body/div[2]/div[3]/div/main/div/div/section[1]/div/h3"
            )
            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.login-button")
                )
            ).click()

            # login goes to https://online-qa.ucsd.edu/dashboard
            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located((By.ID, "footerLogo"))
            )
            # 10 | verifyElementPresent | id=my-courses |  | Verify Courses Panel Loaded
            elements = self.driver.find_elements(By.ID, "my-courses")
            assert len(elements) > 0

        except Exception:
            raise

    def login_sso(self):
        try:
            self.driver.get(self.BASE_URL)

            # pj added for sauce
            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located((By.ID, "main"))
            )

            # 2 | verifyElementPresent | id=main |  | Verify Welcome Message Loads
            elements = self.driver.find_elements(By.ID, "main")
            assert len(elements) > 0

            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, "hamburger-menu")
                )
            ).click()

            super().login_sso()

        except Exception:
            raise

    def load_base_url(self):
        try:
            self.driver.get(self.BASE_URL)

            # pj added for sauce
            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located((By.ID, "main"))
            )

            # 2 | verifyElementPresent | id=main |  | Verify Welcome Message Loads
            elements = self.driver.find_elements(By.ID, "main")
            assert len(elements) > 0

        except Exception:
            raise
