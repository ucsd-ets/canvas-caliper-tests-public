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
    BASE_URL = "https://canvas.ucsd.edu"

    def login_sso(self):
        SSO_USERNAME = os.getenv("CANVAS_SSO_USERNAME")
        SSO_PASS = os.getenv("CANVAS_SSO_PASS")

        # goes immediately to SSO page
        WebDriverWait(self.driver, self.SECONDS_WAIT).until(
            expected_conditions.presence_of_element_located((By.ID, "ssousername"))
        )

        self.driver.find_element(By.ID, "ssousername").send_keys(SSO_USERNAME)
        self.driver.find_element(By.ID, "ssopassword").click()
        self.driver.find_element(By.ID, "ssopassword").send_keys(SSO_PASS)
        self.driver.find_element(By.NAME, "_eventId_proceed").click()
        WebDriverWait(self.driver, self.SECONDS_WAIT).until(
            expected_conditions.visibility_of_element_located((By.ID, "footer"))
        )
        elements = self.driver.find_elements(By.ID, "application")
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
    def login_sso(self):
        try:
            self.driver.get(self.BASE_URL)
            self.driver.set_window_size(1247, 573)
            super().login_sso()

        except Exception:
            raise

    def click_hamburger_menu(self):

        try:
            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, "mobile-header-hamburger")
                )
            ).click()
            # account dropdown button
            # xpath = "/html/body/span[1]/span/div/div/span/ul/li[2]/div"
            xpath = "/html/body/span[1]/span/div/div/span/ul/li[2]/div/button/span/span[1]/span/span[2]/span"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath))
            ).click()

            # confirm logout button appears
            xpath = "/html/body/span[1]/span/div/div/span/ul/li[2]/div/div/div/ul/li[11]/form/button"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath))
            )
            assert self.driver.find_element(By.XPATH, xpath).text == "Logout"

        except Exception:
            raise


class MobileBaseTest(BaseTest):
    def login_sso(self):
        try:
            self.driver.get(self.BASE_URL)
            super().login_sso()

        except Exception:
            raise
