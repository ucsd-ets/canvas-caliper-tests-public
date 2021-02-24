<!-- PROJECT LOGO -->
<p>
  <h1 align="center">Canvas Caliper Tests</h1>
    UI tests for the canvas.ucsd.edu platform.  Uses sauce labs for remote testing.
    <br />
    <a href="https://github.com/github_username/repo/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo/issues">Request Feature</a>
</p>

<!-- ABOUT THE PROJECT -->
## About The Project

### Built With

* [pytest]()
* [selenium]()
* [appium]()
* [sauce labs]()
* [jenkins]() Currently configured to not run (refer to configurations /job/canvas-caliper-tests/configure) Future - once test are ready to autorun add a cron job

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* pip
```sh
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```
* virtualenv
```sh
pip3 install virtualenv
```

Installation
############
 
1. Clone the repo, cd to it
```sh
git clone https://github.com/ucsd-ets/canvas-caliper-tests-public.git
cd canvas-caliper-tests-public
```

2. Make a virtual environment dir that git will ignore and start it
(may need to run "sudo /usr/bin/easy_install virtualenv" first)
```sh
python3 -m virtualenv venv
source venv/bin/activate
```

3. Install required packages: pytest, selenium
```sh
python3 -m pip install pytest
python3 -m pip install selenium
```

4. Environment Setup
```MacBook-Pro:canvas-caliper-tests-public mdandrade$ source venv/bin/activate
(venv) MacBook-Pro:canvas-caliper-tests-public mdandrade$ python3 -V
Python 3.6.12

(venv) MacBook-Pro:canvas-caliper-tests-public mdandrade$ pip list
Package            Version
------------------ ---------
attrs              20.3.0
canvasapi          2.1.0
certifi            2020.12.5
chardet            4.0.0
idna               2.10
importlib-metadata 3.4.0
iniconfig          1.1.1
packaging          20.8
pip                21.0.1
pluggy             0.13.1
py                 1.10.0
pyparsing          2.4.7
pytest             6.2.2
pytz               2020.5
requests           2.25.1
selenium           3.141.0
setuptools         51.3.3
toml               0.10.2
typing-extensions  3.7.4.3
urllib3            1.26.3
wheel              0.36.2
zipp               3.4.0
```

<!-- USAGE EXAMPLES -->
## Usage
```sh
cd test
python -m pytest -m desktop --device=desktop --browser=chrome <file>.py -k <test>
```

<!-- RESULTS -->
## Viewing Test Results on Sauce Labs
Contact the contact person below to get access to the ETS Sauce Labs account.  View the test reults at https://app.saucelabs.com/dashboard/tests/vdc.  View the test stats at https://app.saucelabs.com/analytics/test-overview.

<!-- NEW TESTS -->
## Adding New Caliper Event Generation Tests 
New test classes go in the canvas-caliper-tests-public/test/ subdir.  Classes subclass DesktopBaseTest.  Desktop method names should include "caliper" and end with _desktop() argument to use pytest.mark to run the respective tests.

## Resources
<ul>
    <li><a href="https://canvas.ucsd.edu/courses/20774"> Canvas Caliper Test Course</a></li>
    <li>https://github.com/ucsd-ets/canvas-caliper-tests-public/wiki</li>
    <li>https://github.com/ucsd-ets/canvas-caliper-tests-public</li>
    <li>https://github.com/ucfopen/canvasapi</li>
    <li>https://canvasapi.readthedocs.io/en/stable/getting-started.html</li>
    <li>https://canvas.ucsd.edu/doc/api/live#!/courses.json</li>
</ul>

<!-- CONTACT -->
## Contact
Paul Jamason (pjamason@ucsd.edu)
