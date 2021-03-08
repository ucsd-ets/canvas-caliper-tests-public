from basetest import BaseTest, DesktopBaseTest
import re
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
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
            super().wait_for_ajax(self.driver)
            self.driver.get("https://canvas.ucsd.edu/courses/20774/assignments")

            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//a[@title='Add Assignment to Assignments']")))

            # click on add assigmnent
            # can't get this to work ON SAFARI 11 - new paget not loading
            # safari shows "your browser does not meet the minimum requirements
            # for Canvas" message
            xpath = "//a[@title='Add Assignment to Assignments']"

            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable((By.XPATH, xpath))
            ).click()

            super().wait_for_ajax(self.driver)

            WebDriverWait(self.driver, 7).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//input[@name='name']")))

            self.driver.find_element(
                By.XPATH, "//span[text()='close']/following::input").send_keys("Test1A")
            # Save assignment
            self.driver.find_element(By.XPATH, "//form[@id='ui-id-2']/div[1]/div[2]/button[4]").click()

            super().wait_for_ajax(self.driver)

            elements = self.driver.find_elements(By.LINK_TEXT, "Test1A")
            assert len(elements) > 0

            self.driver.find_element(By.ID, "search_term").send_keys("Test1A")
            # Click 3 dot
            self.driver.find_element(By.XPATH, "//li[contains(@class,'assignment search_show')]//div[contains(@class,'ig-admin')]/div/button").click()
            # Click edit
            self.driver.find_element(By.XPATH, "//li[@class='ui-menu-item']//a").click()

            super().wait_for_ajax(self.driver)
            # Select More Options button
            actions = ActionChains(self.driver) 
            actions.send_keys(Keys.TAB * 4).send_keys(Keys.ENTER)
            actions.perform()
            super().wait_for_ajax(self.driver)

            # Switch to iframe
            elements = self.driver.find_elements(By.XPATH, "//iframe[@id='assignment_description_ifr']")
            assert len(elements) > 0

            ## You have to switch to the iframe like so: ##
            self.driver.switch_to.frame("assignment_description_ifr")

            # Add content to body
            self.driver.find_element(By.ID, "tinymce").send_keys("Edit Body")

            ## Switch back to the "default content" (that is, out of the iframes) ##
            self.driver.switch_to.default_content()
            self.__assignment_override(3)
            super().wait_for_ajax(self.driver)

            elements = self.driver.find_elements(By.XPATH, "//td[text()='Canvas Caliper Events Testing']")
            assert len(elements) > 0
            
            self.driver.find_element(By.XPATH, "//a[@class='btn edit_assignment_link']").click()
            super().wait_for_ajax(self.driver)           
            self.__assignment_override(2)
            super().wait_for_ajax(self.driver)

            elements = self.driver.find_elements(By.XPATH, "//td[text()='Everyone']")
            assert len(elements) > 0

            self.driver.find_element(By.XPATH, "//a[@class='btn edit_assignment_link']").click()
            super().wait_for_ajax(self.driver) 
            self.driver.find_element(By.XPATH, "//button[@class='al-trigger btn']").click()
            self.driver.find_element(By.XPATH, "//a[contains(@class,'delete_assignment_link ui-corner-all')]").click()

            assert self.driver.switch_to.alert.text == "Are you sure you want to delete this assignment?"
            self.driver.switch_to.alert.accept()
            super().wait_for_ajax(self.driver)

            self.driver.find_element(By.ID, "search_term").send_keys("Test1A")
            elements = self.driver.find_elements(By.XPATH, "//a[text()='Test1A']")
            assert len(elements) == 0

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    def test_canvas_copy_course_event_caliper_desktop(self):
        try:

            super().login_sso()

            #
            # delete copied course if it exists
            #

            # click courses
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "global_nav_courses_link")
                )
            ).click()
            # check if any couress under unpublished
            # course xpath
            # xpath = "/html/body/div[3]/span/span/div/div/div/div/div/ul[2]/li/a"

            # get unpub list of courses if it exists
            unpublished_courses = self.driver.find_elements_by_link_text(
                'Unpublished Courses')
            if not unpublished_courses:
                print("No element found")
            else:
                element = unpublished_courses[0]
                elementList = element.find_elements_by_tag_name(
                    "li")

                # loop over list
                for element in elementList:
                    if ("Canvas Caliper Events Testing"):
                        element.click()
                        # wait for course page page to load, click it
                        WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                            expected_conditions.element_to_be_clickable(
                                (By.CLASS_NAME, "settings")
                            )
                        )
                        # click settings link
                        WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                            expected_conditions.element_to_be_clickable((By.CLASS_NAME, "settings")
                                                                        )).click()

                        # click delete this course trash icon
                        WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                            expected_conditions.element_to_be_clickable(
                                (By.CLASS_NAME, "icon-trash")
                            )
                        ).click()

                        # wait for confirm delete page to load; click delete submit button
                        WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                            expected_conditions.element_to_be_clickable(
                                (By.XPATH, "//button[id ='value']")
                            )
                        ).click()

            #
            # get to test course
            #
            # self.__access_test_events_course()

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

            # wait for page to load, click settings in left navbar
            xpath = "//a[@href='/courses/20774/settings']"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.XPATH, xpath)
                )
            )
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable((By.XPATH, xpath))
            ).click()

            #
            # wait for page to load, click on copy course
            #
            WebDriverWait(self.driver, self.SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "course_public_description")
                )
            )
            xpath = "//a[@href='/courses/20774/copy']"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable((By.XPATH, xpath))
            ).click()

            # wait for form visible
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "course_enrollment_term_id")
                )
            )

            # scroll to bottom
            super().scroll_to_bottom()

            # use default values
            # click copy course button
            # self.driver.find_element_by_xpath("//button[id ='value']").click()
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/form/div[8]/button"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable((By.XPATH, xpath))
            ).click()

            # takes user to import content page
            # takes a whilt for course to be created so check for an delete them when we start this test

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    # caliper events
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/enrollment_created.json
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/enrollment_updated.json
    def test_canvas_enrollment_event_caliper_desktop(self):
        try:
            super().login_sso()

            self.__access_test_events_course()

            # click people in course
            # this is off screen, may need presence instead of visiblity
            # self.driver.find_element(By.LINK_TEXT, "People").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.LINK_TEXT, "People"))
            ).click()

            # wait for testacct1 to show
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "user_114217"))
            )

            # remove testacct222 if in course
            if self.driver.find_elements_by_css_selector('#user_115752'):
                print("testacct2 user exists, remove")
                self.__remove_user_from_course()

            #
            # add testacct222 user to course
            #

            # 7 | click | id=addUsers |
            # self.driver.find_element(By.ID, "addUsers").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "addUsers"))
            ).click()

            # click in the add users text field
            # does this id stay the same over time? no
            # 8 | click | id=ugxK2UObCuVx |
            # self.driver.find_element(By.ID, "ugxK2UObCuVx").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.TAG_NAME, "textarea"))
            ).click()

            # enter email address
            # 9 | type | id=ugxK2UObCuVx | testacct222@ucsd.edu
            self.driver.find_element(By.TAG_NAME, "textarea").send_keys(
                "testacct222@ucsd.edu")

            # click next
            # 10 | click | id=addpeople_next |
            self.driver.find_element(By.ID, "addpeople_next").click()

            # wait for "start over" button to appear since page content basically the same
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "addpeople_back"))
            )

            # click "add users" - same id as previous dialog we submitted
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "addpeople_next"))
            ).click()

            # assertion that user is there
            assert self.driver.find_elements_by_css_selector('#user_115752')

            # comment out remove user - keep them there for enrollment change test below
            # still on people page
            # remove user from course
            # self.__remove_user_from_course()

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    # enrollment_state: active, etc.  for a change event, set to deactivate
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/enrollment_state_created.json
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/enrollment_state_updated.json

    def test_canvas_enrollment_state_change_event_caliper_desktop(self):
        try:
            super().login_sso()

            self.__access_test_events_course()

            # click people in course nav menu
            # this is off screen, may need presence instead of visiblity
            # self.driver.find_element(By.LINK_TEXT, "People").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.LINK_TEXT, "People"))
            ).click()

            # wait for testacct1 to show
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "user_114217"))
            )

            #
            # deactivate user
            #

            # click hamburger menu for user
            # 12 | mouseOver | css=#user_115752 .icon-more |
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#user_115752 .icon-more"))
            ).click()
            # element = self.driver.find_element(
            #    By.CSS_SELECTOR, "#user_115752 .icon-more")
            # super().move_to_element(element)

            # 13 | click | css=#user_115752 .icon-more |
            # self.driver.find_element(By.CSS_SELECTOR, "#user_115752 .icon-more").click()
            # 14 | mouseOut | css=#user_115752 .icon-more |
            # element = self.driver.find_element(By.CSS_SELECTOR, "body")
            # actions = ActionChains(self.driver)
            # actions.move_to_element(element, 0, 0).perform()

            super().scroll_to_bottom()

            # click "deactivate user" in dropdown
            # TODO: change to descriptive id in case order changes?
            # 15 | click | id=ui-id-6 |
            element = self.driver.find_element(By.ID, "ui-id-8")
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "ui-id-8"))
            ).click()

            # 22 | assertConfirmation | Are you sure you want to deactivate...
            assert self.driver.switch_to.alert.text == "Are you sure you want to deactivate this user? They will be unable to participate in the course while inactive."

            # 23 | webdriverChooseOkOnVisibleConfirmation |  |
            self.driver.switch_to.alert.accept()

            '''
            # role change code - removed
            # click role dropdown
            # 16 | click | id=role_id |
            # self.driver.find_element(By.ID, "role_id").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "role_id"))
            ).click()

            # select Observer role
            # 17 | select | id=role_id | label=Observer
            dropdown = self.driver.find_element(By.ID, "role_id")

            # TODO: wait for dropdown elements first?
            dropdown.find_element(By.XPATH, "//option[. = 'Observer']").click()

            # submit role change
            # 18 | click | css=.btn-primary > .ui-button-text |
            self.driver.find_element(
                By.CSS_SELECTOR, ".btn-primary > .ui-button-text").click()
            '''

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    # groups (referred to as categories in caliper docs, element ids)
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/group_category_created.json
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/group_created.json
    def test_canvas_group_events_caliper_desktop(self):
        try:
            super().login_sso()

            self.__access_test_events_course()

            # click people in course
            # this is off screen, may need presence instead of visiblity
            # self.driver.find_element(By.LINK_TEXT, "People").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.LINK_TEXT, "People"))
            ).click()

            # wait for testacct1 to show
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "user_114217"))
            )

            #
            # delete group set if if exists
            #
            elements = self.driver.find_elements_by_link_text(
                'Group Set A')
            if not elements:
                print("No Group Set A element found, skip delete")
            else:
                # group_cat_1_element = elements[0]
                WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                    expected_conditions.element_to_be_clickable(
                        (By.LINK_TEXT, "Group Set A"))
                ).click()
                # super().wait_for_ajax(self.driver)

                # click hamburger menu for group set A
                # NOTE: group set A must be first group set listed
                #
                # (//i[@class='icon-more']
                WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                    expected_conditions.element_to_be_clickable(
                        (By.XPATH, "(//a[@role='button']//i)[2]"))
                ).click()
                super().wait_for_ajax(self.driver)

                # click delete group set
                # (//li[@class='ui-menu-item']//a)[3]
                # div#group_categories_tabs>div:nth-of-type(3)>div>div>div>div>span>ul>li:nth-of-type(4)>a
                # //a[contains(@class,'icon-trash delete-category')]
                super().wait_for_ajax(self.driver)
                WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                    expected_conditions.element_to_be_clickable(
                        (By.CSS_SELECTOR, "div#group_categories_tabs>div:nth-of-type(3)>div>div>div>div>span>ul>li:nth-of-type(4)>a"))
                ).click()

                # click "Everyone" tab so we're back at base groups page
                # super().wait_for_ajax(self.driver)
                WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                    expected_conditions.element_to_be_clickable(
                        (By.LINK_TEXT, "Everyone"))
                ).click()

                super().wait_for_ajax(self.driver)
                assert self.driver.switch_to.alert.text == "Are you sure you want to remove this group set?"
                self.driver.switch_to.alert.accept()
                '''
                # delete group - not needed

                # click hamburger menu for group 1
                # (//i[@class='icon-more'])[2]
                # //a[@class='al-trigger action-darkgray']//i[1]
                # //a[@id='group-37446-actions']/i[1]
                WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                    expected_conditions.element_to_be_clickable(
                        (By.XPATH, "//a[@id='group-37446-actions']/i[1]"))
                ).click()

                # By.LINK_TEXT, "Delete"
                # (//li[@class='ui-menu-item']//a)[3]
                # //a[contains(@class,'icon-trash delete-category')]
                super().wait_for_ajax(self.driver)

                WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                    expected_conditions.element_to_be_clickable(
                        (By.XPATH, "(//li[@class='ui-menu-item']//a)[3]"))
                ).click()

                assert self.driver.switch_to.alert.text == "Are you sure you want to remove this group?"
                self.driver.switch_to.alert.accept()
                '''

            # add group set and group
            self.__add_group_set_and_group()

            # assert "Group Set A" exists
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.LINK_TEXT, "Group Set A"))
            ).click()
            elements = self.driver.find_elements_by_link_text(
                'Group Set A')
            assert len(elements) == 1

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/group_membership_created.json
    def test_canvas_group_membership_event_caliper_desktop(self):
        try:
            super().login_sso()

            self.__access_test_events_course()

            # click people in course
            # this is off screen, may need presence instead of visiblity
            # self.driver.find_element(By.LINK_TEXT, "People").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.LINK_TEXT, "People"))
            ).click()

            # wait for testacct1 to show
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "user_114217"))
            )

            # delete membership if it exists
            # drag user out of group cat a

            source_element = self.driver.find_element(
                By.CLASS_NAME, "group-user-name")
            dest_element = self.driver.find_element(
                By.CLASS_NAME, "no-results")
            ActionChains(self.driver).drag_and_drop(
                source_element, dest_element).perform()

            # Click People
            # people
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.CLASS_NAME, "people"))
            ).click()

            #
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.CLASS_NAME, "search-query"))
            )

            #
            # drag student into group
            # we have manually added testacct222 to course already

            source_element = self.driver.find_element(
                By.CLASS_NAME, "group-user-name")
            dest_element = self.driver.find_element(
                By.CLASS_NAME, "group-name")
            ActionChains(self.driver).drag_and_drop(
                source_element, dest_element).perform()

        except Exception as e:
            print("exception")
            print(e)
            assert 0
            self.driver.quit()

    #
    # private utility methods
    #

    def __remove_user_from_course(self):
        try:

            # click user hamburger menu
            # 19 | click | css=#user_115752 .icon-more |
            # self.driver.find_element(By.CSS_SELECTOR, "#user_115752 .icon-more").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#user_115752 .icon-more"))
            ).click()

            super().scroll_to_bottom()

            # click "delete user" in dropdown; changed to 9 from 18
            # 21 | click | id=ui-id-18 |
            # self.driver.find_element(By.ID, "ui-id-18").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "ui-id-9"))
            ).click()

            # 22 | assertConfirmation | Are you sure you want to remove this user? |
            assert self.driver.switch_to.alert.text == "Are you sure you want to remove this user?"

            # 23 | webdriverChooseOkOnVisibleConfirmation |  |
            self.driver.switch_to.alert.accept()

        except Exception:
            raise Exception

    def __add_group_set_and_group(self):
        try:

            # click "+ group set"
            # (By.XPATH, "#//a[@href='/courses/20774/groups#new']"))
            # //button[@id='add-group-set']
            # (By.ID, "add-group-set"))
            # //a[@href='/courses/20774/groups#new']
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "//a[@href='/courses/20774/groups#new']"))
            ).click()

            # click in "group set name" text field
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "new_category_name"))
            ).click()

            # enter "group set a" nane
            self.driver.find_element(
                By.ID, "new_category_name").send_keys("Group Set A")

            # click first radio button
            # //input[@name='split_groups']
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "//input[@name='split_groups']"))
            ).click()

            # click up button on number of groups
            # //input[@name='create_group_count']
            # WebDriverWait(self.driver, super().SECONDS_WAIT).until(
            #    expected_conditions.element_to_be_clickable(
            #        (By.NAME, "create_group_count"))
            # ).click()

            # self.driver.find_element(
            #    By.NAME, "create_group_count").send_keys("1")

            # click "i'll create groups later" - can't get create_group_count option to work
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "(//input[@type='radio'])[3]"))
            ).click()

            # click save button
            # creates new group set
            # newGroupSubmitButton
            super().scroll_to_bottom()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "newGroupSubmitButton"))
            ).click()

            # create group in group set so we can drag students to it
            super().wait_for_ajax(self.driver)
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "//button[@title='Add Group']"))
            ).click()

            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "group_name"))
            ).click()

            self.driver.find_element(
                By.ID, "group_name").send_keys("Group 1")

            self.driver.find_element(
                By.ID, "group_max_membership").click()

            self.driver.find_element(
                By.ID, "group_max_membership").send_keys("1")

            # (//button[@type='submit'])[2]
            self.driver.find_element(
                By.XPATH, "(//button[@type='submit'])[2]").click()

        except Exception:
            raise Exception

    def __access_test_events_course(self):
        try:

            # click courses
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "global_nav_courses_link")
                )
            ).click()

            # click courses
            # self.driver.find_element_by_link_text("Courses").click()

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

        except Exception:
            raise Exception

    def __assignment_override(self, index_number):
        try:

            # assignment override - replace 'Everyone' with section
            # click 'x' for 'Everyone' in 'assign to' box
            # FAILING here (wasn't before): not seeing "everyone " selected after we save it previously
            # TODO: check for it before attempting to delete?
            element = self.driver.find_element(
                By.CLASS_NAME, "ic-token-delete-button")
            super().move_to_element(element)
            element.click()

            # wait for div (not select-based) section list dropdown
            super().wait_for_ajax(self.driver)

            # sections: course name is //*[@id="ic-tokeninput-list-1"]/div[3]
            # everybody is [2]
            xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/form/div[1]/div[6]/div[2]/div/div/div/div[1]/div[2]/ul/li/div/div/div[" + str(
                index_number) + "]"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (
                        By.XPATH, xpath
                        # By.XPATH,'//*[@id="ic-tokeninput-list-1"]/div[' +
                        # str(index_number) + ']',
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

            # Save changes
            # Select More Options button
            actions = ActionChains(self.driver) 
            actions.send_keys(Keys.TAB * 18).send_keys(Keys.ENTER)
            actions.perform()

        except Exception:
            raise Exception
