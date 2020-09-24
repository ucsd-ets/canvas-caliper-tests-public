import pytest
import os

# The request parameter refers to the test session, as fixture functions can accept the request object
# to introspect the “requesting” test function, class, module or session, depending on the scope.
# set scope to function so pytest_runtest_makereport() gets called on function calls
# and we can test the output there
@pytest.fixture(scope="function")
def driver_init(request):
    import os
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    test_name = request.node.name

    # from https://github.com/saucelabs-sample-test-frameworks/Python-Pytest-Selenium/blob/master/conftest.py
    # can't get this to work for multiple browsers - need to run in parallel?

    # credit card test is slow due to one card digit at a time
    # idleTimeout must be greater than webdriver timeouts (basetest.py SECONDS_WAIT) or they dont throw exceptoins

    desired_caps = {}
    # "recordScreenshots": "false",
    # "extendedDebugging": "false",

    desired_caps['videoUploadOnPass'] = "true"
    desired_caps['name'] = request.node.name
    desired_caps['commandTimeout'] = 30
    desired_caps['idleTimeout'] = 15
    desired_caps['recordVideo'] = "true"

    if (os.getenv('device') == 'desktop'):

        desired_caps['build'] = "OpenEdX-UI-QA-desktop"
        desired_caps['tags'] = ["online-qa.ucsd.edu",
                                "ui", "qa", "acceptance", "desktop"]
        desired_caps['maxDuration'] = 150  # get soa test > 90 sec

        if (os.getenv('browser') == 'chrome'):
            desired_caps['browserName'] = "chrome"
            desired_caps['version'] = "latest-1"
            desired_caps['platform'] = "Mac OS X 10.15"
        elif(os.getenv('browser') == 'safari'):
            desired_caps['browserName'] = "safari"
            # downgraded from "latest" and 10.15 on 2020-08-14 due to test_soa function error
            # selenium.common.exceptions.InvalidArgumentException: Message: Request body does not contain required parameter 'handle'.
            # see https://github.com/SeleniumHQ/selenium/issues/6431
            desired_caps['version'] = "11"
            desired_caps['platform'] = "Mac OS X 10.13"
        elif(os.getenv('browser') == 'firefox'):
            desired_caps['browserName'] = "firefox"
            desired_caps['version'] = "latest-1"
            # no jquery in ff on windows
            desired_caps['platform'] = "Mac OS X 10.15"
            # getting java would like to record popup
            desired_caps['recordScreenshots'] = "false"
            desired_caps['recordVideo'] = "false"
        elif(os.getenv('browser') == 'edge'):
            desired_caps['browserName'] = "MicrosoftEdge"
            desired_caps['version'] = "latest-1"
            desired_caps['platform'] = "Windows 10"
        else:
            print("BAD")
            pytest.exit("unsupported browser: " + os.getenv('browser') +
                        "; supported desktop browsers: chrome | safari | edge | firefox")

    # http://appium.io/docs/en/writing-running-appium/web/mobile-web/
    elif(os.getenv('device') == 'mobile'):
        # chrome not supported on ios simulator

        desired_caps['build'] = "OpenEdX-UI-QA-mobile"
        desired_caps['tags'] = ["online-qa.ucsd.edu",
                                "ui", "qa", "acceptance", "mobile"]
        #desired_caps['appiumVersion'] = "1.17.1"
        if (os.getenv('browser') == 'chrome'):
            desired_caps['browserName'] = "Chrome"
            desired_caps['deviceName'] = "Android Emulator"
            desired_caps['platformVersion'] = "8.0"
            desired_caps['platformName'] = "Android"
        elif(os.getenv('browser') == 'safari'):
            desired_caps['browserName'] = "Safari"
            desired_caps['deviceName'] = "iPhone XS Simulator"
            desired_caps['platformVersion'] = "13.2"
            desired_caps['platformName'] = "iOS"
        else:
            pytest.exit("unsupported browser: " + os.getenv('browser') +
                        "; supported mobile browsers: chrome | safari")
        # super slow
        desired_caps['maxDuration'] = 180

    else:
        pytest.exit("unsupported device: " + os.getenv('device') +
                    "; supported devices: desktop | mobile")

    # The command_executor tells the test to run on Sauce, while the desired_capabilities
    # parameter tells us which browsers and OS to spin up.

    web_driver = webdriver.Remote(
        "http://"+os.getenv("SAUCE_USERNAME")+":" +
        os.getenv("SAUCE_ACCESS_KEY")+"@ondemand.saucelabs.com:80/wd/hub",
        desired_capabilities=desired_caps)

    # https://www.blazemeter.com/blog/improve-your-selenium-webdriver-tests-with-pytest/
    # for every test class object that is decorated with @pytest.mark.userfixtures("driver_init")
    # we set the attribute "driver". So in the test class we can access the web driver
    # instance with self.driver. You can notice that we haven't setup the WebDriver instance
    # implicitly, instead we are just using it via reference to the self.driver.
    # This is the implementation of the dependency injection:
    # in the test class or function we don't know how the WebDriver was initialized
    # or what is going to be happen later, we are just using the instance.
    session = request.node
    # for item in session.items:
    #    cls = item.getparent(pytest.Class)
    #    setattr(cls.obj,"driver",web_driver)
    request.cls.driver = web_driver

    # This is specifically for SauceLabs plugin.
    # In case test fails after selenium session creation having this here will help track it down.
    # creates one file per test non ideal but xdist is awful
    if web_driver is not None:
        print(
            "SauceOnDemandSessionID={} job-name={}".format(web_driver.session_id, test_name))
    else:
        raise WebDriverException("Never created!")

    # yield # provide the fixture value to test methods
    yield web_driver

    # Teardown starts here
    # report results
    # use the test result to send the pass/fail status to Sauce Labs
    sauce_result = "failed" if request.node.rep_call.failed else "passed"
    print("sauce_result: " + sauce_result)
    web_driver.execute_script("sauce:job-result={}".format(sauce_result))
    web_driver.quit()  # teardown; this gets called after tests are complete


def set_test_status(jobid, passed):
    import os
    import json
    import base64
    import http.client
    # base64string = base64.encodestring(('%s:%s' % (os.getenv("SAUCE_USERNAME"),os.getenv("SAUCE_ACCESS_KEY"))).encode()).decode().strip()
    # base64bytes = base64.encodebytes(('%s:%s' % (os.getenv("SAUCE_USERNAME"),os.getenv("SAUCE_ACCESS_KEY"))).encode())
    base64string = str(base64.b64encode(bytes('%s:%s' % (
        os.getenv("SAUCE_USERNAME"), os.getenv("SAUCE_ACCESS_KEY")), 'utf-8')))[1:]
    body_content = json.dumps({"passed": passed})
    connection = http.client.HTTPConnection("saucelabs.com")
    connection.request('PUT', '/rest/v1/%s/jobs/%s' % (os.getenv("SAUCE_USERNAME"), jobid),
                       body_content,
                       headers={"Authorization": "Basic %s" % base64string})
    result = connection.getresponse()
    # pj return true if result.staus is 200
    return result.status == 200


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for Sauce Labs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield

    # this object looks like
    # <TestReport 'test_enrollCourseAuditor.py::TestEnrollCourseAuditor::test_test1login_non_sso' when='call' outcome='passed'>
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)


def pytest_addoption(parser):
    # todo: os type
    parser.addoption('--device', action='store',
                     default='desktop', help='[desktop | mobile]')
    parser.addoption('--browser', action='store',
                     default='chrome', help='[safari | chrome | firefox | edge')

# set global variables


def pytest_configure(config):
    os.environ["device"] = config.getoption('device')
    #pytest.device = config.getoption('device')
    os.environ["browser"] = config.getoption('browser')
    #pytest.browser = config.getoption('browser')
    # print(pytest.browser)


# @pytest.fixture
# def device():
#    # return "ios"
#    return os.environ["device"]

# @pytest.fixture(autouse=True)
# def skip_by_device(request, device):
#    if request.node.get_closest_marker('skip_device'):
#        if request.node.get_closest_marker('skip_device').args[0] == device:
#            pytest.skip('skipped on this device: {}'.format(device))

# uses -m arg to only run tests with desktop/mobile in function name based on given arg
def pytest_collection_modifyitems(items):
    for item in items:
        if "desktop" in item.nodeid:
            item.add_marker(pytest.mark.desktop)
        elif "mobile" in item.nodeid:
            item.add_marker(pytest.mark.mobile)
