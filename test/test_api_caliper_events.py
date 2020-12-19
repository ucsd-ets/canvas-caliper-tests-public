import sys
import os
import canvasapi
import pytest
# Import the Canvas class
from canvasapi import Canvas
from canvasapi.submission import GroupedSubmission, Submission
from canvasapi.upload import Uploader
from canvasapi.assignment import (
    Assignment,
    AssignmentGroup,
    AssignmentOverride,
    AssignmentExtension,
)
from canvasapi.course import Course, CourseNickname, LatePolicy, Page

from canvasapi.group import Group, GroupCategory, GroupMembership


class TestCaliperGeneration():

    @pytest.fixture(autouse=True)
    def prepare_canvas(self):

        # Canvas API URL
        self.API_URL = "https://canvas.ucsd.edu"
        # Canvas API key
        self.API_KEY = os.getenv("CANVAS_API_KEY")
        # 115753: testacct3
        # only used in test_submit_file - TODO confirm required
        self.USER_ID = 115753
        # test caliper events course (pjamason and testacct1 teachers)
        self.COURSE_ID = 20774
        self.ASSIGNMENT_ID = 192792
        # Initialize a new Canvas object
        self.canvas = Canvas(self.API_URL, self.API_KEY)
        self.requester = self.canvas._Canvas__requester
        self.course = self.canvas.get_course(self.COURSE_ID)

        yield
        self.canvas = False

    # group category, group, membership created
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/group_category_created.json
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/group_membership_created.json

    def test_create_group_membership(self, prepare_canvas):
        self.group_category = self.course.create_group_category(
            "Cat From API 3")
        print(self.group_category)
        group_name = "Group 1"
        self.group = self.group_category.create_group(name=group_name)
        print(self.group)
        response = self.group.create_membership(self.USER_ID)
        print(response)
        # confirm return object is of type GroupMembership
        assert isinstance(response, GroupMembership)

        # note: https://github.com/ucfopen/canvasapi/blob/develop/tests/test_group.py
        # test_get_membership also checks that creating membership via user object (instead of id)
        # returns GM instance type

        response = self.group_category.delete()
        print(response)

    def test_enrollment_created(self, prepare_canvas):
        # create file
        self.file = open(self.filename, "w+")
        uploader = Uploader(self.requester, "upload_response", self.file)
        result = uploader.start()

        assert(result[0])
        assert isinstance(result[1], dict)
        assert "url" in result[1]

        # close file(s)
        self.file.close()

    # submission created
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/submission_created.json
    # see test_submit() in assignment https://github.com/ucfopen/canvasapi/blob/develop/tests/test_assignment.py

    def test_submit_file(self, prepare_canvas):

        # pjamason can't submit to own course
        # caliper events test 2 course (testacct1 teacher)
        self.COURSE_ID = 24284
        self.ASSIGNMENT_ID = 241934

        self.canvas = Canvas(self.API_URL, self.API_KEY)
        self.requester = self.canvas._Canvas__requester
        self.course = self.canvas.get_course(self.COURSE_ID)
        self.assignment = self.course.get_assignment(self.ASSIGNMENT_ID)

        filename = "tmp2.png"
        try:
            with open(filename, "w+") as file:
                sub_type = "online_upload"
                sub_dict = {"submission_type": sub_type}
                submission = self.assignment.submit(sub_dict, file)
            assert isinstance(submission, Submission)
            assert submission.submission_type == sub_type
            print(submission)
            print("test")

        except Exception:
            raise Exception

    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/wiki_page_created.json
    def test_create_wiki_page(self, prepare_canvas):
        try:
            # appears to overwrite so no pre-deletion needed
            title = "Newest Page"
            new_page = self.course.create_page(wiki_page={"title": title})

            assert isinstance(new_page, Page)
            assert new_page.title == title
        except Exception:
            raise Exception

    # delete wiki page
    # see https://github.com/ucfopen/canvasapi/blob/cff8028a1f87767f504fcbb4ddeebcd36d68707f/tests/test_page.py
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/wiki_page_deleted.json

    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/wiki_page_updated.json



    # TODO: attachment (file) created
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/attachment_created.json
    # def test_upload_file(self, prepare_canvas):

    # TODO: attachment (file) created
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/attachment_deleted.json
    # def test_delete_file

    # file updated
    # attachment (file) created
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/attachment_updated.json
    # NOT WORKING: cant requeset token in Uploader

    def test_update_file(self, prepare_canvas):

        self.filename = "test_upload.txt"
        # create file
        self.file = open(self.filename, "w+")
        uploader = Uploader(self.requester, "upload_response", self.file)
        result = uploader.start()

        assert(result[0])
        assert isinstance(result[1], dict)
        assert "url" in result[1]

        # close file(s)
        self.file.close()

    # attachment (file) downloaded
    # NOT A CALIPER EVENT

    def test_download_file(self, prepare_canvas):

        self.file = self.course.get_files()[0]
        try:
            self.file.download("canvasapi_file_download_test.txt")
            assert os.path.exists("canvasapi_file_download_test.txt")
            # with open("canvasapi_file_download_test.txt") as downloaded_file:
            #    self.assertEqual(downloaded_file.read(), '"file contents are here"')
        finally:
            try:
                os.remove("canvasapi_file_download_test.txt")
            except OSError:
                pass
