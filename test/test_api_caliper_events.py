import sys
import os
import canvasapi
import pytest
# Import the Canvas class
from canvasapi import Canvas
from canvasapi.exceptions import RequiredFieldMissing, ResourceDoesNotExist
from canvasapi.submission import GroupedSubmission, Submission
from canvasapi.upload import Uploader
from canvasapi.requester import Requester
from canvasapi.util import combine_kwargs, is_multivalued, obj_or_id
from canvasapi.user import User
from canvasapi.discussion_topic import DiscussionTopic

from canvasapi.assignment import (
    Assignment,
    AssignmentGroup,
    AssignmentOverride,
    AssignmentExtension,
)
from canvasapi.quiz import (
    Quiz,
    QuizAssignmentOverrideSet,
    QuizExtension,
    QuizQuestion,
    QuizReport,
    QuizStatistic,
    QuizSubmission,
    QuizSubmissionEvent,
    QuizSubmissionQuestion,
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

        # Ensure that the user-supplied access token and base_url contain no leading or
        # trailing spaces that might cause issues when communicating with the API.
        #access_token = access_token.strip()
        #base_url = get_institution_url(base_url)

        self._requester = Requester(self.API_URL, self.API_KEY)
        # production account
        self.UCSD_PROD_ACCOUNT = 1

        # 115753: testacct3
        # only used in test_submit_file - TODO confirm required
        self.USER_ID = 115753
        # test caliper events course (pjamason and testacct1 teachers)
        self.COURSE_ID = 20774
        self.ASSIGNMENT_ID = 192792  # week 1 assignment
        self.TESTACCT444_NUMERIC_ID = 122382

        # Initialize a new Canvas object
        self.canvas = Canvas(self.API_URL, self.API_KEY)

        self.requester = self.canvas._Canvas__requester
        self.course = self.canvas.get_course(self.COURSE_ID)
        self.account = self.canvas.get_account(self.UCSD_PROD_ACCOUNT)

        # TODO add a cleanup here so we don't have to test for/delete pages

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

    # create wiki page
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/wiki_page_created.json

    # update wiki page - no ucf method; from UI only?  use a different page than above
    # https://community.canvaslms.com/t5/Question-Forum/Update-Wiki-Page-HTML-via-API/td-p/67550
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/wiki_page_updated.json
    def test_create_update_wiki_page(self, prepare_canvas):
        # delete if it exists, otherwise will create "Newest Page-2"
        url = "newest-page"
        self.page_course = None
        try:
            self.page_course = self.course.get_page(url)
        except:
            if (self.page_course and isinstance(self.page_course, Page)):
                deleted_page = self.__delete_wiki_page()
                assert isinstance(deleted_page, Page)

        title = "Newest Page"
        new_page = self.course.create_page(wiki_page={"title": title})

        assert isinstance(new_page, Page)
        # title gets appended to with integer, can't test
        #assert new_page.title == title

        # ucf create_page() uses canvas REST wiki create api:
        # https://github.com/ucfopen/canvasapi/blob/master/canvasapi/course.py
        # https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.create
        # use a local version of this that uses .update
        #
        #updated_page = self.__update_wiki_page_body(new_page,wiki_page={"body": "<h1>new wiki body</h1>"})
        updated_page = self.__update_wiki_page_body(new_page)

        assert isinstance(updated_page, Page)

    # delete wiki page
    # see https://github.com/ucfopen/canvasapi/blob/cff8028a1f87767f504fcbb4ddeebcd36d68707f/tests/test_page.py
    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/wiki_page_deleted.json

    def test_delete_wiki_page(self, prepare_canvas):
        url = "newest-page"
        self.page_course = self.course.get_page(url)
        #page = self.page_course
        #deleted_page = page.delete()
        deleted_page = self.__delete_wiki_page()
        assert isinstance(deleted_page, Page)

    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/user_account_association_created.json
    # if they are assigned that unique id
    def test_create_and_delete_user(self, prepare_canvas):
        unique_id = "testacct444"
        created_user = self.account.create_user({"unique_id": unique_id})

        assert isinstance(created_user, User)
        # print(created_user)
        assert created_user.login_id == unique_id

        deleted_user = self.account.delete_user(created_user)
        assert isinstance(deleted_user, User)

    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/discussion_topic_created.json
    def test_create_and_delete_discussion_topic(self, prepare_canvas):

        title_str = "Test Topic 2"
        discussion = self.course.create_discussion_topic(
            # topic={"title": title})
            title=title_str)

        print(discussion)
        assert isinstance(discussion, DiscussionTopic)
        assert (hasattr(discussion, "course_id"))
        assert title_str == discussion.title

        response = discussion.delete()

    def test_reply_discussion_topic(self, prepare_canvas):

        topic_id = 250552  # test topic 1
        discussion = self.course.get_discussion_topic(topic_id)

        # print(discussion)
        assert isinstance(discussion, DiscussionTopic)
        assert (hasattr(discussion, "course_id"))

        entry = discussion.post_entry()
        print(entry)

    # grade change
    # via user assignment score change
    def test_grade_change_assignment(self, prepare_canvas):
        assignment = self.course.get_assignment(self.ASSIGNMENT_ID)

        submission = assignment.get_submission(self.USER_ID)
        score = 5
        submission.edit(submission={'posted_grade': score})

        submission = assignment.get_submission(self.USER_ID)
        score = 7
        submission.edit(submission={'posted_grade': score})
        print(Submission)
        assert int(submission.grade) == score

    # https://d1raj86qipxohr.cloudfront.net/production/caliper/event-types/asset_accessed.json
    def test_asset_accessed_get_page(self, prepare_canvas):

        url = "start-here"
        page = self.course.get_page(url)

        assert isinstance(page, Page)

    #########
    # below not working

    # try a quiz submission
    # NOT WORKING what to use for ids?
    def test_grade_change_quiz(self, prepare_canvas):
        submission = QuizSubmission(
            self.canvas._Canvas__requester,
            {
                "id": 1,
                "quiz_id": 34289,  # use week 1 quiz in course
                "user_id": self.USER_ID,
                "course_id": self.COURSE_ID,
                "submission_id": 1,
                "attempt": 3,
                "validation_token": "this is a validation token",
                "manually_unlocked": None,
                "score": 7,
            },
        )

        print(submission)

        returned_submission = submission.update_score_and_comments(
            quiz_submissions=[
                {
                    "attempt": 1,
                    "fudge_points": 1,
                    "questions": {
                        "question id 1": {"score": 1, "comment": "question 1 comment"},
                        "question id 2": {"score": 2, "comment": "question 2 comment"},
                        "question id 3": {"score": 3, "comment": "question 3 comment"},
                    },
                }
            ]
        )

        assert isinstance(returned_submission, QuizSubmission)
        #self.assertTrue(hasattr(submission, "id"))
        #self.assertTrue(hasattr(submission, "attempt"))
        #self.assertTrue(hasattr(submission, "quiz_id"))
        #self.assertTrue(hasattr(submission, "validation_token"))
        #self.assertEqual(submission.score, 7)

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

    def __delete_wiki_page(self):

        page = self.page_course
        deleted_page = page.delete()
        return deleted_page

    def __update_wiki_page_body(self, wiki_page, **kwargs):
        # def create_page(self, wiki_page, **kwargs):
        """
        update a wiki page.
        :calls: `POST /api/v1/courses/:course_id/pages \
        <https://canvas.instructure.com/doc/api/pages.html#method.wiki_pages_api.update>`_
        :param wiki_page: The title for the page.
        :type wiki_page: object, not dict
        :returns: The created page.
        :rtype: :class:`canvasapi.page.Page`
        """

        print(wiki_page.title)
        # if isinstance(wiki_page, dict) and "title" in wiki_page:
        if isinstance(wiki_page, Page) and hasattr(wiki_page, 'title'):
            wiki_page_dict = vars(wiki_page)
            wiki_page_dict["body"] = "<h1>new wiki body</h1>"
            kwargs["wiki_page"] = wiki_page_dict
            print(kwargs)
        else:
            #raise RequiredFieldMissing("Dictionary with key 'title' is required.")
            raise RequiredFieldMissing(
                "Object of type Page with attribute 'title' is required.")

        response = self._requester.request(
            "POST", "courses/{}/pages".format(self.COURSE_ID), _kwargs=combine_kwargs(**kwargs)
        )

        page_json = response.json()
        page_json.update({"course_id": self.COURSE_ID})

        return Page(self._requester, page_json)
