#!/usr/bin/env python


#  Copyright 2013-2014 NaviNet Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import httplib
import base64
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidElementStateException
from robot.libraries.BuiltIn import BuiltIn
from applitools import logger
from applitools.logger import StdoutLogger
from applitools.geometry import Region
from applitools.eyes import Eyes, BatchInfo
from applitools.utils import _image_utils
from applitools._webdriver import EyesScreenshot
from applitools.target import Target, IgnoreRegionBySelector, FloatingRegionBySelector, FloatingBounds
from version import VERSION

_version_ = VERSION
ROBOT_LIBRARY_VERSION = VERSION


def get_search_element(selector):
    try:
        return getattr(By, selector.upper())
    except AttributeError:
        raise InvalidElementStateException('Please select a valid selector: CSS_SELECTOR, XPATH, ID, LINK_TEXT,'
                                           'PARTIAL_LINK_TEXT, NAME, TAG_NAME, CLASS_NAME')


def check_logging(includeEyesLog, httpDebugLog):
    if includeEyesLog is True:
        logger.set_logger(StdoutLogger())
        logger.open_()
    if httpDebugLog is True:
        httplib.HTTPConnection.debuglevel = 1


class RobotAppEyes:
    """
    Robot-AppEyes is a visual verfication library for Robot Framework that leverages
    the Eyes-Selenium.

    *Before running tests*

    Prior to running tests, RobotAppEyes must first be imported into your Robot test suite.

    Example:
        | Library | RobotAppEyes |

    In order to run the Robot-AppEyes library and return results, you have to create a free account https://applitools.com/sign-up/ with Applitools.
    You can retreive your API key from the applitools website and that will need to be passed in your Open Eyes Session keyword.

    *Using Selectors*

    Using the keyword Check Eyes Region By Element. The first four strategies are supported: _CSS SELECTOR_, _XPATH_, _ID_ and _CLASS NAME_.

    Using the keyword Check Eyes Region By Selector. *All* the following strategies are supported:

    | *Strategy*        | *Example*                                                                                                     | *Description*                                   |
    | CSS_SELECTOR      | Check Eyes Region By Selector `|` CSS_SELECTOR      `|` .first.expanded.dropdown `|`  CssElement              | Matches by CSS Selector                         |
    | XPATH             | Check Eyes Region By Selector `|` XPATH             `|` //div[@id='my_element']  `|`  XpathElement            | Matches with arbitrary XPath expression         |
    | ID                | Check Eyes Region By Selector `|` ID                `|` my_element               `|`  IdElement               | Matches by @id attribute                        |
    | CLASS_NAME        | Check Eyes Region By Selector `|` CLASS_NAME        `|` element-search           `|`  ClassElement            | Matches by @class attribute                     |
    | LINK_TEXT         | Check Eyes Region By Selector `|` LINK_TEXT         `|` My Link                  `|`  LinkTextElement         | Matches anchor elements by their link text      |
    | PARTIAL_LINK_TEXT | Check Eyes Region By Selector `|` PARTIAL_LINK_TEXT `|` My Li                    `|`  PartialLinkTextElement  | Matches anchor elements by partial link text    |
    | NAME              | Check Eyes Region By Selector `|` NAME              `|` my_element               `|`  NameElement             | Matches by @name attribute                      |
    | TAG_NAME          | Check Eyes Region By Selector `|` TAG_NAME          `|` div                      `|`  TagNameElement          | Matches by HTML tag name                        |
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def open_eyes_session(self,
                          appname,
                          testname,
                          apikey,
                          applitoolsurl='https://eyessdk.applitools.com',
                          library='Selenium2Library',
                          width=None,
                          height=None,
                          osname=None,
                          browsername=None,
                          matchlevel=None,
                          includeEyesLog=False,
                          httpDebugLog=False,
                          fullPageScreenshot=False,
                          baselineName=None,
                          batchName=None,
                          branchname=None,
                          parentbranch=None):
        """
        Starts a session with the Applitools Eyes Website.
        Arguments:
                |  Application Name (string)                    | The name of the application under test.                                                                     |
                |  Test Name (string)                           | The test name.                                                                                              |
                |  API Key (string)                             | User's Applitools Eyes key.
                |  library  (optional)                          | Standard:Selenium2Library. If you use another one, assign the right library.
                |  applitoolsurl (optional)                     | Standard:eyes.applitools.com. If you run in a cloud version, assign the right applitoolsurl.
                |  (Optional) Width (int)                       | The width of the browser window e.g. 1280                                                                   |
                |  (Optional) Height (int)                      | The height of the browser window e.g. 1000                                                                  |
                |  (Optional) Operating System (string)         | The operating system of the test, can be used to override the OS name to allow cross OS verfication         |
                |  (Optional) Browser Name (string)             | The browser name for the test, can be used to override the browser name to allow cross browser verfication  |
                |  (Optional) Match Level (string)              | The match level for the comparison - can be STRICT, LAYOUT or CONTENT                                       |
                |  Force Full Page Screenshot (default=False)   | Will force the browser to take a screenshot of whole page.                                      |
                |  Include Eyes Log (default=False)             | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.                    |
                |  HTTP Debug Log (default=False)               | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable.              |
                |  baselineName (default=None)                  | New tests will be automatically saved as baseline.
                |  batchName (default=None)                     | Tests with the same batchname will be unified as one group in the Test Manager screen.
                |  Branch Name (default=False)                  | The branch to use to check test                                                                             |
                |  Parent Branch (default=False)                | Parent Branch to base the new Branch on
                |  Force full page screenshot (default=false)   | The whole page will be in the screen shot

        Creates an instance of the library webdriver.
        Defines a global driver and sets the library webdriver to the global driver.
        Checks if there has been a width or height value passed in.
        If there no are values passed in, eyes calls the method open without the width and height values.
        Otherwise eyes calls open with the width and height values defined.
        The Height resolution should not be greater than 1000, this is currently Applitools maximum setting.
        Starts a session with the Applitools Eyes Website. See https://eyes.applitools.com/app/sessions/
        Example:
        | *Keywords*         |  *Parameters*        |               |                  |                       |           |        |        |                  |                      |                     |                     |                       |
        | Open Browser       |  yourTestingUrl      |  gc           |                  |                       |           |        |        |                  |                      |                     |                     |                       |
        | Open Eyes Session  | yourAppName          |  yourTestName | YourApplitoolsKey|  cloudapplitoolsurl   | library   |  1024  |  768   |  OSOverrideName  |  BrowserOverrideName |  matchlevel=LAYOUT  | includeEyesLog=True |  httpDebugLog=True    |
        | Check Eyes Window  |  NaviNet Home        |               |                  |                       |           |        |        |                  |                      |                     |                     |                       |
        | Close Eyes Session |  False               |               |                  |                       |           |        |        |                  |                      |                     |                     |                       |
        """
        global driver
        global eyes
        eyes = Eyes(applitoolsurl)
        eyes.api_key = apikey
        eyes.force_full_page_screenshot = fullPageScreenshot
        s2l = BuiltIn().get_library_instance(library)
        webdriver = s2l._current_browser()
        driver = webdriver

        if includeEyesLog is True:
            logger.set_logger(StdoutLogger())
            logger.open_()
        if httpDebugLog is True:
            httplib.HTTPConnection.debuglevel = 1
        if osname is not None:
            eyes.host_os = osname  # (str)
        if browsername is not None:
            eyes.host_app = browsername  # (str)
        if baselineName is not None:
            eyes.baseline_name = baselineName  # (str)
        if batchName is not None:
            batch = BatchInfo(batchName)
            eyes.batch = batch
        if matchlevel is not None:
            eyes.match_level = matchlevel
        if parentbranch is not None:
            eyes.parent_branch_name = parentbranch  # (str)
        if branchname is not None:
            eyes.branch_name = branchname  # (str)
        if width is None and height is None:
            eyes.open(driver, appname, testname)
        else:
            intwidth = int(width)
            intheight = int(height)
            eyes.open(driver, appname, testname, {'width': intwidth, 'height': intheight})

    def check_eyes_window(self, name, includeEyesLog=False, httpDebugLog=False):
        """
        Takes a snapshot from the browser using the web driver and matches it with
        the expected output.
        Arguments:
                |  Name (string)                                | Name that will be given to region in Eyes.                                                      |
                |  Include Eyes Log (default=False)             | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.        |
                |  HTTP Debug Log (default=False)               | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable.  |
        Example:
        | *Keywords*         |  *Parameters*        |               |                   |       |       |
        | Open Browser       |  yourTestingUrl      | gc            |                   |       |       |
        | Open Eyes Session  |  yourAppName         | yourTestName  | YourApplitoolsKey |  1024 |  768  |
        | Check Eyes Window  |  NaviNet Home        | True          |                   |       |       |
        | Close Eyes Session |  False               |               |                   |       |       |
        """
        check_logging(includeEyesLog, httpDebugLog)

        eyes.check_window(name)

    def check_eyes_region(self, element, width, height, name, includeEyesLog=False, httpDebugLog=False):
        """
        Takes a snapshot of the given region from the browser using the web driver to locate an xpath element
        with a certain width and height and matches it with the expected output.
        The width and the height cannot be greater than the width and the height specified in the open_eyes_session keyword.
        Arguments:
                |  Element (string)                 | This needs to be passed in as an xpath e.g. //*[@id="navbar"]/div/div                          |
                |  Width (int)                      | The width of the region that is tested e.g. 500                                                |
                |  Height (int)                     | The height of the region that is tested e.g. 120                                               |
                |  Name (string)                    | Name that will be given to region in Eyes.                                                     |
                |  Include Eyes Log (default=False) | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.       |
                |  HTTP Debug Log (default=False)   | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable. |
        Example:
        | *Keywords*         |  *Parameters*                |               |                   |                   |       |
        | Open Browser       |  yourTestingUrl              | gc            |                   |                   |       |
        | Open Eyes Session  | yourAppName                  | yourTestName  | YourApplitoolsKey |  1024             |  768  |
        | Check Eyes Region  |  //*[@id="navbar"]/div/div   | 500           |  120              |  NaviNet Navbar   |       |
        | Close Eyes Session |  False                       |               |                   |                   |       |
        """
        check_logging(includeEyesLog, httpDebugLog)

        intwidth = int(width)
        intheight = int(height)

        searchElement = driver.find_element_by_xpath(element)
        location = searchElement.location
        region = Region(location["x"], location["y"], intwidth, intheight)
        eyes.check_region(region, name)

    def check_eyes_region_by_element(self, selector, value, name, includeEyesLog=False, httpDebugLog=False):
        """
        Takes a snapshot of the region of the given selector and element value from the browser using the web driver
        and matches it with the expected output. With a choice from four selectors, listed below, to check by.
        Arguments:
                |  Selector (string)                | This will decide what element will be located. The supported selectors include: XPATH, ID, CLASS NAME, CSS SELECTOR  |
                |  Value (string)                   | The specific value of the selector. e.g. an xpath value //*[@id="navbar"]/div/div                                    |
                |  Name (string)                    | Name that will be given to region in Eyes.                                                                           |
                |  Include Eyes Log (default=False) | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.                             |
                |  HTTP Debug Log (default=False)   | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable.                       |
        Example:
        | *Keywords*                    |  *Parameters*     |               |                       |       |       |
        | Open Browser                  |  yourTestingUrl   | gc            |                       |       |       |
        | Open Eyes Session             | yourAppName       | yourTestName  | YourApplitoolsKey     |  1024 |  768  |
        | Check Eyes Region By Element  |  CLASS_NAME       | container     | NaviNetClassElement   |       |       |
        | Close Eyes Session            |  False            |               |                       |       |       |
        """
        check_logging(includeEyesLog, httpDebugLog)

        if selector.upper() == 'XPATH':
            searchElement = driver.find_element_by_xpath(value)
        elif selector.upper() == 'ID':
            searchElement = driver.find_element_by_id(value)
        elif selector.upper() == 'CLASS NAME':
            searchElement = driver.find_element_by_class_name(value)
        elif selector.upper() == 'CSS SELECTOR':
            searchElement = driver.find_element_by_css_selector(value)
        else:
            raise InvalidElementStateException('Please select a valid selector: XPATH, ID, CLASS NAME, CSS SELECTOR')
        eyes.check_region_by_element(searchElement, name)

    def check_eyes_region_by_selector(self, selector, value, name, includeEyesLog=False, httpDebugLog=False):
        """
        Takes a snapshot of the region of the element found by calling find_element(by, value) from the browser using the web driver
        and matches it with the expected output. With a choice from eight selectors, listed below to check by.
        Arguments:
                |  Selector (string)                | This will decide what element will be located. The supported selectors include: CSS SELECTOR, XPATH, ID, LINK TEXT, PARTIAL LINK TEXT, NAME, TAG NAME, CLASS NAME.    |
                |  Value (string)                   | The specific value of the selector. e.g. a CSS SELECTOR value .first.expanded.dropdown                                                                                |
                |  Name (string)                    | Name that will be given to region in Eyes.                                                                                                                            |
                |  Include Eyes Log (default=False) | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.                                                                              |
                |  HTTP Debug Log (default=False)   | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable.                                                                        |
        Example:
        | *Keywords*                    |  *Parameters*        |                            |                       |       |       |
        | Open Browser                  |  yourTestingUrl      | gc                         |                       |       |       |
        | Open Eyes Session             | yourAppName          | yourTestName               | YourApplitoolsKey     |  1024 |  768  |
        | Check Eyes Region By Selector |  CSS SELECTOR        |  .first.expanded.dropdown  |  NaviNetCssElement    |       |       |
        | Close Eyes Session            |  False               |                            |                       |       |       |
        """
        check_logging(includeEyesLog, httpDebugLog)
        searchElement = get_search_element(selector)

        eyes.check_region_by_selector(searchElement, value, name)

    def compare_image(self, path, imagename=None, ignore_mismatch=False, includeEyesLog=False, httpDebugLog=False):
        """
        Select an image and send it to Eyes for comparison. A name can be used in place of the image's file name.
        Arguments:
                |  Path                             | Path of the image to send to eyes for visual comparison.                                                                   |
                |  imagename (default=None)         | Can manually set the name desired for the image passed in. If no name is passed in it will default file name of the image. |
                |  Include Eyes Log (default=False) | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.                                   |
                |  HTTP Debug Log (default=False)   | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable.                             |
        Example:
        | *Keywords*         |  *Parameters*                |                       |                   |       |       |
        | Open Browser       |  yourTestingUrl              | gc                    |                   |       |       |
        | Open Eyes Session  |  yourAppName                 | yourTestName          | YourApplitoolsKey |  1024 |  768  |
        | Compare Image      |  selenium-screenshot-1.png   |  Image Name Example   |                   |       |       |
        | Close Eyes Session |                              |                       |                   |       |       |
        """
        if imagename is None:
            tag = os.path.basename(path)
        else:
            tag = imagename

        eyes._prepare_to_check()
        check_logging(includeEyesLog, httpDebugLog)

        with open(path, 'rb') as image_file:
            screenshot64 = image_file.read().encode('base64')
            screenshot = _image_utils.png_image_from_bytes(base64.b64decode(screenshot64))
            screenshotBytes = EyesScreenshot.create_from_image(screenshot, eyes._driver)
        title = eyes.get_title()
        app_output = {'title': title, 'screenshot64': None}
        user_inputs = []
        prepare_match_data = eyes._match_window_task._create_match_data_bytes(
            app_output, user_inputs, tag, ignore_mismatch, screenshotBytes)
        eyes._match_window_task._agent_connector.match_window(
            eyes._match_window_task._running_session, prepare_match_data)

    def close_eyes_session(self, includeEyesLog=False, httpDebugLog=False):
        """
        Closes a session and returns the results of the session.
        If a test is running, aborts it. Otherwise, does nothing.
        The RobotAppEyesTest.txt test will fail after the first run, this is because a baseline is being created and will be accepted automatically by Applitools Eyes.
        A second test run will show a successful comparison between screens and the test will pass.
        Arguments:
                |  Include Eyes Log (default=False) | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.        |
                |  HTTP Debug Log (default=False)   | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable.  |
        Example:
        | *Keywords*                    | *Parameters*      |               |                            |       |       |
        | Open Browser                  | yourTestingUrl    | gc            |                            |       |       |
        | Open Eyes Session             | yourAppName       | yourTestName  | YourApplitoolsKey          |  1024 |  768  |
        | Check Eyes Region By Selector | LINK_TEXT         | RESOURCES     |  NaviNetLinkTextElement    |       |       |
        | Close Eyes Session            |                   |               |                            |       |       |
        """
        check_logging(includeEyesLog, httpDebugLog)

        eyes.close()
        eyes.abort_if_not_closed()

    def eyes_session_is_open(self):
        """
        Returns True if an Applitools Eyes session is currently running, otherwise it will return False.
        | *Keywords*         |  *Parameters*            |                       |                   |       |       |
        | Open Browser       |  yourTestingUrl          | gc                    |                   |       |       |
        | Open Eyes Session  | yourAppName              | yourTestName          | YourApplitoolsKey |  1024 |  768  |
        | ${isOpen}=         |  Eyes Session Is Open    |                       |                   |       |       |
        | Run Keyword If     |  ${isOpen}==True         | Close Eyes Session    |                   |       |       |
        """
        return eyes.is_open()

    def select_eyes_ignore_region_by_selector(self, selector, value, includeEyesLog=False, httpDebugLog=False):
        """
        Selects the element, which should be ignored in the comparison. In the screenshot you can see a border around that element.
        Arguments:
                |  Selector (string)                | This will decide what element will be located. The supported selectors include: CSS SELECTOR, XPATH, ID, LINK TEXT, PARTIAL LINK TEXT, NAME, TAG NAME, CLASS NAME.    |
                |  Value (string)                   | The specific value of the selector. e.g. a CSS SELECTOR value .first.expanded.dropdown.                                                                               |                                                                                                                          |
                |  Include Eyes Log (default=False) | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.                                                                              |
                |  HTTP Debug Log (default=False)   | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable.                                                                        |

        Example:
        | *Keywords*                            |  *Parameters*     |                |                   |      |       |
        | Open Browser                          |  yourTestingUrl   | gc             |                   |      |       |
        | Open Eyes Session                     | yourAppName       | yourTestName   | YourApplitoolsKey | 1024 |  768  |
        | Select Eyes Ignore Region By Selector |  ID               |  search-input  |                   |      |       |
        | Close Eyes Session                    |                   |                |                   |      |       |
        """

        check_logging(includeEyesLog, httpDebugLog)

        searchElement = get_search_element(selector)

        target = Target().ignore(IgnoreRegionBySelector(searchElement, value))
        eyes.check_window(target=target)

    def select_eyes_floating_region_by_selector(self, selector, value, left, up, right, down, includeEyesLog=False,
                                                httpDebugLog=False):
        """
        Selects the element, which could be floating on the page. Then you have assign the floating area. In the screenshot you can see a border around that element and a second
        boarder which is the floating area.
        Arguments:
                |  Selector (string)                | This will decide what element will be located. The supported selectors include: CSS SELECTOR, XPATH, ID, LINK TEXT, PARTIAL LINK TEXT, NAME, TAG NAME, CLASS NAME.    |
                |  Value (string)                   | The specific value of the selector. e.g. a CSS SELECTOR value .first.expanded.dropdown.                                                                               |                                                                                                                          |
                |  up       (int)                   | These four variables are making the border around the element where the floating element can move.                                                                                       |
                |  down     (int)                   |                                                                                                                                                                       |
                |  Left     (int)                   |                                                                                                                                                                       |
                |  Right    (int)                   |                                                                                                                                                                       |
                |  Include Eyes Log (default=False) | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.                                                                              |
                |  HTTP Debug Log (default=False)   | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable.                                                                        |

        Example:
        | *Keywords*                                |  *Parameters*        |               |                   |       |       |    |
        | Open Browser                              |  yourTestingUrl      | gc            |                   |       |       |    |
        | Open Eyes Session                         | yourAppName          | yourTestName  | YourApplitoolsKey |  1024 |  768  |    |
        | Select Eyes Floating Region By Selector   |  ID                  |  search-input |  20               | 10    | 20    | 10 |
        | Close Eyes Session                        |                      |               |                   |       |       |    |
        """

        check_logging(includeEyesLog, httpDebugLog)

        searchElement = get_search_element(selector)

        floating = Target().floating(
            FloatingRegionBySelector(searchElement, value, FloatingBounds(left, up, right, down)))
        eyes.check_window(target=floating)

