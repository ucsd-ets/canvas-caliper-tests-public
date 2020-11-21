import sys
import os
import canvasapi
import pytest
# Import the Canvas class
from canvasapi import Canvas
from canvasapi.upload import Uploader
from canvasapi.assignment import (
    Assignment,
    AssignmentGroup,
    AssignmentOverride,
    AssignmentExtension,
)


class TestCaliperGeneration():

    @pytest.fixture(autouse=True)
    def prepare_canvas(self):

        # Canvas API URL
        self.API_URL = "https://canvas.ucsd.edu"
        # Canvas API key
        self.API_KEY = os.getenv("CANVAS_API_KEY")
        # Initialize a new Canvas object
        self.canvas = Canvas(self.API_URL, self.API_KEY)
        self.requester = self.canvas._Canvas__requester
        self.course = self.canvas.get_course(20774)

        yield
        self.canvas = False

    # group category created
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/group_category_created.json
    def test_create_group_category(self, prepare_canvas):
        self.group_category = self.course.create_group_category(
            "Cat From API")
        response = self.group_category.delete()
        print(response)

    # group created
    def test_create_group(self, prepare_canvas):
        self.group_category = self.course.create_group_category(
            "Cat From API")
        self.group_category.create_group()
        response = self.group_category.delete()
        print(response)

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

    def test_enrollment_created(self, prepare_canvas)
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
    # NOT AN EVENT

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

    # submission created
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/submission_created.json
    # TODO
    def test_submit(self, prepare_canvas):

        sub_type = "online_upload"
        sub_dict = {"submission_type": sub_type}
        submission = self.assignment.submit(sub_dict)

        #self.assertIsInstance(submission, Submission)
        #self.assertTrue(hasattr(submission, "submission_type"))
        #self.assertEqual(submission.submission_type, sub_type)

    # submission created (file)
    #      # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/submission_created.json
    # NOT WORKING
    # NOT WORKING: could not get submission to appear
    # TODO: api call to SAH to confirm generation
    def test_submit_file(self, prepare_canvas):

        # get "test assignment 1"
        self.assignment = self.course.get_assignment(219410)

        # see https://github.com/ucfopen/canvasapi/blob/develop/tests/test_assignment.py
        # 115753: testacct3
        user_id = 115753
        filename = "tmp2.png"
        try:
            with open(filename, "w+") as file:
                response = self.assignment.upload_to_submission(file, user_id)

            # self.assertTrue(response[0])
            assert response[0] is True

            #self.assertIsInstance(response[1], dict)
            assert type(response[1]) is dict

            #            self.assertIn("url", response[1])
            assert "url" in response[1]

            print(response[0])
            print(response[1])
            print("test")

        except Exception:
            raise Exception
