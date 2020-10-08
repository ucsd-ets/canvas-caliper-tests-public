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
    def test_canvas_logged_in_event_caliper_desktop(self):
        try:
            super().login_sso()

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    def test_canvas_logged_out_event_caliper_desktop(self):
        try:
            super().login_sso()

            # click account
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "global_nav_profile_link")
                )
            ).click()

            # click logout
            xpath = "/html/body/div[3]/span/span/div/div/div/div/div/span/form/button"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, xpath))
            )
            assert self.driver.find_element(By.XPATH, xpath).text == "Logout"

            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, xpath))
            ).click()

            # logout goes to ucsd.edu
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located(
                    (By.CLASS_NAME, "navbar-header")
                )
            )
            assert (self.driver.current_url) == "https://www.ucsd.edu/"

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    def test_canvas_assignment_events_caliper_desktop(self):
        try:
            super().login_sso()

            # click account
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "global_nav_profile_link")
                )
            ).click()

            # click courses
            self.driver.find_element_by_link_text("Courses").click()

            # wait for test course div
            xpath = "/html/body/div[3]/span/span/div/div/div/div/div/ul[1]/li[1]/a"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.XPATH, xpath))
            )

            # click on test course
            self.driver.find_element_by_link_text(
                "Canvas Caliper Events Testing"
            ).click()

            # wait for page to load, click assignments in left navbar
            xpath = "/html/body/div[2]/div[2]/div[2]/div[2]/nav/ul/li[5]/a"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    # (By.CLASS_NAME, "assignments")
                    (By.XPATH, xpath)
                )
            )

            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable((By.XPATH, xpath))
            ).click()

            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.CLASS_NAME, "assignment_group")
                )
            )

            # click on add assigmnent
            # can't get this to work ON SAFARI 11 - new paget not loading
            # safari shows "your browser does not meet the minimum requirements
            # for Canvas" message
            xpath = '//*[@title="Add Assignment"]'

            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable((By.XPATH, xpath))
            ).click()

            # wait for assignment name input field visible
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/div[1]/div/input"

            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    # (By.ID, "assignment_name")
                    (By.XPATH, xpath)
                )
            )

            # click in assignment name input field, set assign name
            self.driver.find_element(By.ID, "assignment_name").click()
            # self.driver.find_element(By.XPATH, xpath).click()
            self.driver.find_element(
                By.ID, "assignment_name").send_keys("Test Assignment 1")

            # click "text entry" checkbox in "online entry options"
            # self.driver.find_element(By.ID, "assignment_text_entry").click()
            element = self.driver.find_element(By.ID, "assignment_text_entry")
            super().move_to_element(element)
            element.click()

            # save assignment (EVENT: assignment_created)
            super().scroll_to_bottom()
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/form/div[3]/div[2]/button[3]"
            element = self.driver.find_element(By.XPATH, xpath)
            super().move_to_element(element)

            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable((By.XPATH, xpath))
            ).click()

            # assignment override - edit, modify assign groups, save
            self.__assignment_override(3)

            # assignment override updated - edit, modify assign groups, save
            self.__assignment_override(2)

            # TODO delete assignment

            # wait for page with edit assignment button to load, click it
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div[1]/div[2]/a"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    # (By.CLASS_NAME, "edit_assigment_link"))
                    (By.XPATH, xpath))
            ).click()

            # wait for page to load, check for an element unique to this page (dot menu is
            # on preceding page too):
            # wait for assignment name input field visible
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/div[1]/div/input"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    # (By.ID, "assignment_name")
                    (By.XPATH, xpath)
                )
            )

            # click dot menu
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div/div[2]/div/button"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, xpath))
                # (By.CLASS_NAME, "icon-more"))
            ).click()

            # click delete assignment
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div/div[2]/div/ul/li/a"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    # (By.CLASS_NAME, "delete_assigment_link"))
                    (By.XPATH, xpath))
            ).click()

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    def __assignment_override(self, index_number):
        try:

            # wait for page with edit assignment button to load, click it
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div[1]/div[2]/a"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    # (By.CLASS_NAME, "edit_assigment_link"))
                    (By.XPATH, xpath))
            ).click()

            # wait for assign section to load
            # note that it loads, then iframe loads, pushing it down
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, "assign-to-label")
                )
            )

            # assignment override
            # click 'x' in 'assign to'
            element = self.driver.find_element(
                By.CLASS_NAME, "ic-token-delete-button")
            super().move_to_element(element)
            element.click()

            # click in the assign field
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.CLASS_NAME, "ic-tokeninput"))
            ).click()

            # wait for div (not select-based) section list dropdown
            super().wait_for_ajax(self.driver)

            # sections: course name is //*[@id="ic-tokeninput-list-1"]/div[3]
            # everybody is [2]
            # /html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/div[6]/div[2]/div/div/div/div[1]/div[2]/ul/li/div/div/div[2]
            # /html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/div[6]/div[2]/div/div/div/div[1]/div[2]/ul/li/div/div/div[3]
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/div[6]/div[2]/div/div/div/div[1]/div[2]/ul/li/div/div/div[" + str(
                index_number) + "]"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (
                        By.XPATH, xpath
                        # By.XPATH,'//*[@id="ic-tokeninput-list-1"]/div[' +
                        #str(index_number) + ']',
                    )
                )
            ).click()
            super().wait_for_ajax(self.driver)

            # save assignment (EVENT: assignment_updated, assignment_override_created)

            super().scroll_to_bottom()
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/form/div[3]/div[2]/button[3]"
            element = self.driver.find_element(By.XPATH, xpath)
            super().move_to_element(element)

            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable((By.XPATH, xpath))
            ).click()

        except Exception as e:
            raise Exception
