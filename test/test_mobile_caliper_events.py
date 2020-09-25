from basetest import BaseTest, MobileBaseTest
import re
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import os

# Selenium 3.14+ doesn't enable certificate checking
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestMobileCaliperEvents(MobileBaseTest):
    def test_logged_in_event_caliper_mobile(self):
        try:
            super().login_sso()

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    def test_logged_out_event_caliper_mobile(self):
        try:
            super().login_sso()
            print("desktop only")

            super().click_hamburger_menu()

            xpath = "/html/body/span[1]/span/div/div/span/ul/li[2]/div/div/div/ul/li[11]/form/button"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath))
            )
            assert self.driver.find_element(By.XPATH, xpath).text == "Logout"

            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable((By.XPATH, xpath))
            ).click()

            # logout goes to ucsd.edu
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, "navbar-header")
                )
            )
            assert (self.driver.current_url) == "https://ucsd.edu"

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()
