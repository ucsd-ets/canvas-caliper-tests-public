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
            self.__access_test_events_course()

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
            # super().move_to_element(element)
            element.click()

            # save assignment (EVENT: assignment_created)
            # super().scroll_to_bottom()
            #xpath = "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/form/div[3]/div[2]/button[3]"
            #element = self.driver.find_element(By.XPATH, xpath)
            # super().move_to_element(element)

            xpath = "//button[@type='submit']"
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
            #xpath = "/html/body/div[3]/span/span/div/div/div/div/div/ul[2]/li/a"

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
            #self.driver.find_element_by_xpath("//button[id ='value']").click()
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
            #self.driver.find_element(By.LINK_TEXT, "People").click()
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
            #self.driver.find_element(By.ID, "addUsers").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "addUsers"))
            ).click()

            # click in the add users text field
            # does this id stay the same over time? no
            # 8 | click | id=ugxK2UObCuVx |
            #self.driver.find_element(By.ID, "ugxK2UObCuVx").click()
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
            #self.__remove_user_from_course()

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
            #self.driver.find_element(By.LINK_TEXT, "People").click()
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
            #element = self.driver.find_element(
            #    By.CSS_SELECTOR, "#user_115752 .icon-more")
            #super().move_to_element(element)


            # 13 | click | css=#user_115752 .icon-more |
            # self.driver.find_element(By.CSS_SELECTOR, "#user_115752 .icon-more").click()
            # 14 | mouseOut | css=#user_115752 .icon-more |
            #element = self.driver.find_element(By.CSS_SELECTOR, "body")
            #actions = ActionChains(self.driver)
            #actions.move_to_element(element, 0, 0).perform()

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

    # groups
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/group_category_created.json
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/group_created.json
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/group_membership_created.json
    def test_canvas_group_events_caliper_desktop(self):
        try:
            super().login_sso()

            self.__access_test_events_course()

 # click people in course
            # this is off screen, may need presence instead of visiblity
            #self.driver.find_element(By.LINK_TEXT, "People").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.LINK_TEXT, "People"))
            ).click()

            # wait for testacct1 to show
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.XPATH, "user_114217"))
            )

            # TODO delete group set if if exists

            # click "+ group set"
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "#//a[@href='/courses/20774/groups#new']"))
            ).click()

            # click in "new category name" text field
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "new_category_name"))
            ).click()

            # enter "group cat 1" nane
            self.driver.find_element(
                By.ID, "new_category_name").send_keys("Group Cat 1")

            # click first radio button
            # //input[@name='split_groups']
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "//input[@name='split_groups']"))
            ).click()            

            # click up button on number of groups
            # //input[@name='create_group_count']
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "//input[@name='create_group_count']"))
            ).click()                        

            # click save button
            # creates new group category and new group in it
            # newGroupSubmitButton
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.ID, "newGroupSubmitButton"))
            ).click()                        

            # //i[@class='icon-more']
            # click hamburger menu for group 1
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "//i[@class='icon-more']"))
            ).click()  

            # click delete group 
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "ui-id-13"))
            ).click() 

            # 
            # add students to group
            # this requires them accepting invite email sent to user, which we can't do
            # TODO; use api
            
            '''
            # click hamburger menu for group cat 1
            # //a[@class='al-trigger action-darkgray']//i[1]
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "//a[@class='al-trigger action-darkgray']//i[1]"))
            ).click()                        

            # click visit group homepage
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.XPATH, "ui-id-4"))
            ).click() 

            # Click People
            # people
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.element_to_be_clickable(
                    (By.CLASS_NAME, "people"))
            ).click()             
            '''

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
            #self.driver.find_element(By.ID, "ui-id-18").click()
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "ui-id-9"))
            ).click()

            # 22 | assertConfirmation | Are you sure you want to remove this user? |
            assert self.driver.switch_to.alert.text == "Are you sure you want to remove this user?"

            # 23 | webdriverChooseOkOnVisibleConfirmation |  |
            self.driver.switch_to.alert.accept()

        except Exception as e:
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

        except Exception as e:
            raise Exception

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
            # try moving to it again
            WebDriverWait(self.driver, super().SECONDS_WAIT).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, "assign-to-label")
                )
            )
            super().wait_for_ajax(self.driver)
            element = self.driver.find_element(
                By.ID, "assign-to-label")
            super().move_to_element(element)

            # assignment override - replace 'Everyone' with section
            # click 'x' for 'Everyone' in 'assign to' box
            # FAILING here (wasn't before): not seeing "everyone " selected after we save it previously
            # TODO: check for it before attempting to delete?
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
