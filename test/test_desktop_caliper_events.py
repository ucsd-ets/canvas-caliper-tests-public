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
    def test_logged_in_event_caliper_desktop(self):
        try:
            super().login_sso()

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    def test_logged_out_event_caliper_desktop(self):
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
                expected_conditions.presence_of_element_located((By.XPATH, xpath))
            )
            assert self.driver.find_element(By.XPATH, xpath).text == "Logout"

            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located((By.XPATH, xpath))
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

    def test_assignment_events_caliper_desktop(self):
        try:
            super().login_sso()

            # click account
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "global_nav_profile_link")
                    # (By.ID, "ic-app-header__main-navigation")
                )
            ).click()

            # click courses
            self.driver.find_element_by_link_text("Courses").click()

            #
            #
            # WebDriverWait(self.driver, super().SECONDS_WAIT).until(
            #    expected_conditions.element_to_be_clickable(
            #        (By.CLASS_NAME, "fOyUs_bGBk")
            #    )
            # ).click()

            # js only
            # super().wait_for_ajax(self.driver)

            # wait for test course div
            xpath = "/html/body/div[3]/span/span/div/div/div/div/div/ul[1]/li[1]/a"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located((By.XPATH, xpath))
            )

            # click on test course
            self.driver.find_element_by_link_text(
                "Canvas Caliper Events Testing"
            ).click()

            # wait for page to load, click assignments in left navbar
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.CLASS_NAME, "assignments")
                )
            )

            # this fails inconsistently
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.CLASS_NAME, "assignments")
                )
            ).click()

            # click on assignments
            # self.driver.find_element_by_link_text("Assignments").click()

            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.CLASS_NAME, "assignment_group")
                )
            )

            # click on add assigmnent
            xpath = '//*[@title="Add Assignment"]'
            element = self.driver.find_element(By.XPATH, xpath)
            self.move_to_element(element)

            # WebDriverWait(self.driver, super().SECONDS_WAIT).until(
            #    expected_conditions.element_to_be_clickable(
            #        (By.CLASS_NAME, "new_assignment")
            #    )
            # ).click()

            # wait for page to load
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.CLASS_NAME, "assignments")
                )
            )

            # WebDriverWait(self.driver, self.SECONDS_WAIT).until(
            #    expected_conditions.visibility_of_element_located(
            #        (By.ID, "assignment_name")
            #    )
            # )

            element = self.driver.find_element(By.ID, "assignment_name")
            self.move_to_element(element)

            self.driver.find_element(By.ID, "assignment_name").click()
            self.driver.find_element(By.ID, "assignment_name").send_keys(
                "Test Assignment 1"
            )

            # save assignment (EVENT: assignment_created)
            self.driver.find_element_by_link_text("Save").click()

            # WebDriverWait(self.driver, self.SECONDS_WAIT).until(
            #    expected_conditions.element_to_be_clickable(
            #        (By.ID, "assignment_points_possible").click()
            #    )
            # )

            # self.driver.find_element(By.ID, "assignment_points_possible").click()
            # self.driver.find_element(By.ID, "assignment_points_possible").send_keys("1")
            # self.driver.find_element(By.ID, "assignment_points_possible").click()

            # assignment override
            self._assignment_override(3)

            # assignment override updated
            self._assignment_override(2)

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    def __assignment_override(self, index_number):
        try:

            # click edit assignment
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.CLASS_NAME, "edit_assignment_link")
                )
            ).click()

            # assignment override
            # click 'x' in 'assign to'
            self.driver.find_element(By.ID, "ic-token-delete-button").click()

            # wait for div (not select-based) section list dropdown
            super().wait_for_ajax()

            # sections: course name is //*[@id="ic-tokeninput-list-1"]/div[3]
            # everybody is [2]
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="ic-tokeninput-list-1"]/div[' + index_number + "]",
                    )
                )
            ).click()

            # save assignment (EVENT: assignment_updated, assignment_override_created)
            self.driver.find_element_by_link_text("Save").click()

        except Exception as e:
            raise Exception
