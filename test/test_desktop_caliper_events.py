from basetest import BaseTest, DesktopBaseTest
import re
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import os

# Selenium 3.14+ doesn't enable certificate checking
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestDesktopCaliperEvents(DesktopBaseTest):

    def test_edx_bookmark_desktop(self):
        try:
            super().login_sso()

            # Step # | name | target | value | comment
            # 1 | open | /dashboard |  |
            self.driver.get(super().BASE_URL + "/dashboard")
            # 2 | setWindowSize | 1365x713 |  |
            self.driver.set_window_size(1365, 713)

            # Verify Login Successful
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fa-caret-down")))
            elements = self.driver.find_elements(
                By.CSS_SELECTOR, ".login-saml-default")
            assert len(elements) == 0

            elements = self.driver.find_elements(
                By.LINK_TEXT, "Generating Test Events")
            assert len(elements) > 0

            self.driver.find_element(
                By.LINK_TEXT, "Generating Test Events").click()

            elements = self.driver.find_elements(
                By.XPATH, "//div[@id='course-container']/header/div/nav/h2")
            assert len(elements) > 0

            # Click Video link
            self.driver.find_element(
                By.XPATH, "//a[@id='block-v1:same+same1+same+type@vertical+block@06df3f377fb740acb22ffcf4bc2e23f7']/div/div").click()

            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//img[@id='footerLogo']")))

            elements = self.driver.find_elements(
                By.XPATH, "//span[contains(.,'Bookmark this page')]")
            assert len(elements) > 0

            # Add Bookmark
            ### Trigger edx.bookmark.added ###
            self.driver.find_element(
                By.XPATH, "//span[contains(.,'Bookmark this page')]").click()

            elements = self.driver.find_elements(
                By.XPATH, "//span[contains(.,'Bookmarked')]")
            assert len(elements) > 0

            self.driver.find_element(By.LINK_TEXT, "Course").click()

            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//img[@id='footerLogo']")))

            elements = self.driver.find_elements(
                By.XPATH, "//a[contains(@href, '/courses/course-v1:same+same1+same/bookmarks/')]")
            assert len(elements) > 0

            # Acess bookmarks
            ### Trigger edx.bookmark.listed ###
            self.driver.find_element(
                By.XPATH, "//a[contains(@href, '/courses/course-v1:same+same1+same/bookmarks/')]").click()

            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//img[@id='footerLogo']")))

            elements = self.driver.find_elements(
                By.XPATH, "//h3[@id='bookmark-link-0']")
            assert len(elements) > 0

            # Open Bookmark
            ### Trigger edx.bookmark.accessed ###
            self.driver.find_element(
                By.XPATH, "//span[contains(.,'View')]").click()

            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//img[@id='footerLogo']")))

            elements = self.driver.find_elements(
                By.XPATH, "//span[contains(.,'Bookmarked')]")
            assert len(elements) > 0

            # Remove Bookmark
            ### Trigger edx.bookmark.removed ###
            self.driver.find_element(By.CSS_SELECTOR, ".bookmark-text").click()

            super().wait_for_ajax(self.driver)

            elements = self.driver.find_elements(
                By.XPATH, "//span[contains(.,'Bookmark this page')]")
            assert len(elements) > 0

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()
