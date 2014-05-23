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
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidElementStateException
from robot.libraries.BuiltIn import BuiltIn
from applitools import logger
from applitools.logger import StdoutLogger
from applitools.geometry import Region
from applitools.eyes import Eyes
from version import VERSION

_version_ = VERSION


class RobotAppEyes:
    """
    Robot-AppEyes is a visual verfication library for Robot Framework that leverages
    the Eyes-Selenium and Selenium2 libraries.



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
    | CSS SELECTOR      | Check Eyes Region By Selector `|` CSS SELECTOR      `|` .first.expanded.dropdown `|`  CssElement              | Matches by CSS Selector                         |
    | XPATH             | Check Eyes Region By Selector `|` XPATH             `|` //div[@id='my_element']  `|`  XpathElement            | Matches with arbitrary XPath expression         |
    | ID                | Check Eyes Region By Selector `|` ID                `|` my_element               `|`  IdElement               | Matches by @id attribute                        |
    | CLASS NAME        | Check Eyes Region By Selector `|` CLASS NAME        `|` element-search           `|`  ClassElement            | Matches by @class attribute                     |
    | LINK TEXT         | Check Eyes Region By Selector `|` LINK TEXT         `|` My Link                  `|`  LinkTextElement         | Matches anchor elements by their link text      |
    | PARTIAL LINK TEXT | Check Eyes Region By Selector `|` PARTIAL LINK TEXT `|` My Li                    `|`  PartialLinkTextElement  | Matches anchor elements by partial link text    |
    | NAME              | Check Eyes Region By Selector `|` NAME              `|` my_element               `|`  NameElement             | Matches by @name attribute                      |
    | TAG NAME          | Check Eyes Region By Selector `|` TAG NAME          `|` div                      `|`  TagNameElement          | Matches by HTML tag name                        |
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def open_eyes_session(self, url, appname, testname, apikey, width=None,
                          height=None, osname=None, browsername=None,
                          match_level="STRICT", includeEyesLog=True):
        """
        Starts a session with the Applitools Eyes Website.

        Arguments:
                |  URL (string)                         | The URL to start the test on                                                                                |
                |  Application Name (string)            | The name of the application under test.                                                                     |
                |  Test Name (string)                   | The test name.                                                                                              |
                |  API Key (string)                     | User's Applitools Eyes key.                                                                                 |
                |  (Optional) Width (int)               | The width of the browser window e.g. 1280                                                                   |
                |  (Optional) Height (int)              | The height of the browser window e.g. 1000                                                                  |
                |  (Optional) Operating System (string) | The operating system of the test, can be used to override the OS name to allow cross OS verfication         |
                |  (Optional) Browser Name (string)     | The browser name for the test, can be used to override the browser name to allow cross browser verfication  |
                |  (Optional) Match Level (string)      | The match level for the comparison - can be STRICT, LAYOUT or CONTENT                                       |
                |  Include Eyes Log (default=True)      | The Eyes logs will be included by default. To deactivate, pass 'False' in the variable.                     |

        Creates an instance of the Selenium2Library webdriver.
        Defines a global driver and sets the Selenium2Library webdriver to the global driver.

        Checks if there has been a width or height value passed in.
        If there no are values passed in, eyes calls the method open without the width and height values.
        Otherwise eyes calls open with the width and height values defined.

        The Height resolution should not be greater than 1000, this is currently Applitools maximum setting.

        The driver then gets the url that will be tested.

        Starts a session with the Applitools Eyes Website. See https://eyes.applitools.com/app/sessions/

        Example:

        | *Keywords*         |  *Parameters*                                                                                                    |                                                                 |
        | Open Browser       |  http://www.navinet.net/ | gc                |                            |                     |        |       |                  |                       |                      |
        | Open Eyes Session  |  http://www.navinet.net/ | RobotAppEyes_Test |  NaviNet_RobotAppEyes_Test |  YourApplitoolsKey  |  1024  |  768  |  OSOverrideName  |  BrowserOverrideName  |  match_level=LAYOUT  |
        | Check Eyes Window  |  NaviNet Home            |                   |                            |                     |        |       |                  |                       |                      |
        | Close Eyes Session |  False                   |                   |                            |                     |        |       |                  |                       |                      |

        """

        Eyes.api_key = apikey
        s2l = BuiltIn().get_library_instance('Selenium2Library')
        webdriver = s2l._current_browser()
        global driver
        global eyes
        driver = webdriver
        eyes = Eyes()
        if includeEyesLog is True:
            logger.set_logger(StdoutLogger())
        if osname is not None:
            eyes.host_os = osname  # (str)
        if browsername is not None:
            eyes.host_app = browsername  # (str)
        if width is None and height is None:
            eyes.open(driver, appname, testname, match_level=match_level)
        else:
            intwidth = int(width)
            intheight = int(height)
            eyes.open(driver, appname, testname, {'width': intwidth, 'height': intheight}, match_level=match_level)
            driver.get(url)

    def check_eyes_window(self, name, force_full_page_screenshot=False,
                          includeEyesLog=True):
        """
        Takes a snapshot from the browser using the web driver and matches it with
        the expected output.

        Arguments:
                |  Name (string)                                | Name that will be given to region in Eyes.                                                |
                |  Force Full Page Screenshot (default= False)  | Will force the browser to take a screenshot of whole page.                                |
                |  Include Eyes Log (default=True)              | The Eyes logs will be included by default. To deactivate, pass 'False' in the variable.   |

        Example:

        | *Keywords*         |  *Parameters*                                                                                                              |
        | Open Browser       |  http://www.navinet.net/ | gc                |                            |                     |        |       |         |
        | Open Eyes Session  |  http://www.navinet.net/ | RobotAppEyes_Test |  NaviNet_RobotAppEyes_Test |  YourApplitoolsKey  |  1024  |  768  |  False  |
        | Check Eyes Window  |  NaviNet Home            | True              |                            |                     |        |       |         |
        | Close Eyes Session |  False                   |                   |                            |                     |        |       |         |

        """
        if includeEyesLog is True:
            logger.set_logger(StdoutLogger())
        eyes.force_full_page_screenshot = force_full_page_screenshot
        eyes.check_window(name)

    def check_eyes_region(self, element, width, height, name, includeEyesLog=True):
        """
        Takes a snapshot of the given region from the browser using the web driver to locate an xpath element
        with a certain width and height and matches it with the expected output.
        The width and the height cannot be greater than the width and the height specified in the open_eyes_session keyword.

        Arguments:
                |  Element (string)                 | This needs to be passed in as an xpath e.g. //*[@id="navbar"]/div/div                     |
                |  Width (int)                      | The width of the region that is tested e.g. 500                                           |
                |  Height (int)                     | The height of the region that is tested e.g. 120                                          |
                |  Name (string)                    | Name that will be given to region in Eyes.                                                |
                |  Include Eyes Log (default=True)  | The Eyes logs will be included by default. To deactivate, pass 'False' in the variable.   |
        Example:

        | *Keywords*         |  *Parameters*                                                                                                                 |
        | Open Browser       |  http://www.navinet.net/     | gc                |                             |                    |        |       |        |
        | Open Eyes Session  |  http://www.navinet.net/     | RobotAppEyes_Test |  NaviNet_RobotAppEyes_Test  |  YourApplitoolsKey |  1024  |  768  | False  |
        | Check Eyes Region  |  //*[@id="navbar"]/div/div   | 500               |  120                        |  NaviNet Navbar    |        |       |        |
        | Close Eyes Session |  False                       |                   |                             |                    |        |       |        |
        """
        if includeEyesLog is True:
            logger.set_logger(StdoutLogger())

        intwidth = int(width)
        intheight = int(height)

        searchElement = driver.find_element_by_xpath(element)
        location = searchElement.location
        region = Region(location["x"], location["y"], intwidth, intheight)
        eyes.check_region(region, name)

    def check_eyes_region_by_element(self, selector, value, name, includeEyesLog=True):
        """
        Takes a snapshot of the region of the given selector and element value from the browser using the web driver
        and matches it with the expected output. With a choice from four selectors, listed below, to check by.

        Arguments:
                |  Selector (string)                | This will decide what element will be located. The supported selectors include: XPATH, ID, CLASS NAME, CSS SELECTOR  |
                |  Value (string)                   | The specific value of the selector. e.g. an xpath value //*[@id="navbar"]/div/div                                    |
                |  Name (string)                    | Name that will be given to region in Eyes.                                                                           |
                |  Include Eyes Log (default=True)  | The Eyes logs will be included by default. To deactivate, pass 'False' in the variable.                              |
        Example:

        | *Keywords*                    |  *Parameters*                                                                                                              |
        | Open Browser                  |  http://www.navinet.net/  |  gc                |                             |                    |       |      |         |
        | Open Eyes Session             |  http://www.navinet.net/  |  RobotAppEyes_Test |  NaviNet_RobotAppEyes_Test  |  YourApplitoolsKey |  1024 |  768 |  False  |
        | Check Eyes Region By Element  |  CLASS NAME               |  container         |  NaviNetClassElement        |                    |       |      |         |
        | Close Eyes Session            |  False                    |                    |                             |                    |       |      |         |

        """
        if includeEyesLog is True:
            logger.set_logger(StdoutLogger())

        searchElement = None

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

    def check_eyes_region_by_selector(self, selector, value, name, includeEyesLog=True):
        """
        Takes a snapshot of the region of the element found by calling find_element(by, value) from the browser using the web driver
        and matches it with the expected output. With a choice from eight selectors, listed below to check by.

        Arguments:
                |  Selector (string)                | This will decide what element will be located. The supported selectors include: CSS SELECTOR, XPATH, ID, LINK TEXT, PARTIAL LINK TEXT, NAME, TAG NAME, CLASS NAME.    |
                |  Value (string)                   | The specific value of the selector. e.g. a CSS SELECTOR value .first.expanded.dropdown                                                                                |
                |  Name (string)                    | Name that will be given to region in Eyes.                                                                                                                            |
                |  Include Eyes Log (default=True)  | The Eyes logs will be included by default. To deactivate, pass 'False' in the variable.                                                                               |
        Example:

        | *Keywords*                    |  *Parameters*                                                                                                                      |
        | Open Browser                  |  http://www.navinet.net/  |  gc                       |                            |                    |        |       |         |
        | Open Eyes Session             |  http://www.navinet.net/  |  RobotAppEyes_Test        |  NaviNet_RobotAppEyes_Test |  YourApplitoolsKey |  1024  |  768  |  False  |
        | Check Eyes Region By Selector |  CSS SELECTOR             |  .first.expanded.dropdown |  NaviNetCssElement         |                    |        |       |         |
        | Close Eyes Session            |  False                    |                           |                            |                    |        |       |         |

        """
        if includeEyesLog is True:
            logger.set_logger(StdoutLogger())
        searchElement = None

        if selector.upper() == 'CSS SELECTOR':
            searchElement = By.CSS_SELECTOR
        elif selector.upper() == 'XPATH':
            searchElement = By.XPATH
        elif selector.upper() == 'ID':
            searchElement = By.ID
        elif selector.upper() == 'LINK TEXT':
            searchElement = By.LINK_TEXT
        elif selector.upper() == 'PARTIAL LINK TEXT':
            searchElement = By.PARTIAL_LINK_TEXT
        elif selector.upper() == 'NAME':
            searchElement = By.NAME
        elif selector.upper() == 'TAG NAME':
            searchElement = By.TAG_NAME
        elif selector.upper() == 'CLASS NAME':
            searchElement = By.CLASS_NAME
        else:
            raise InvalidElementStateException('Please select a valid selector: CSS SELECTOR, XPATH, ID, LINK TEXT, PARTIAL LINK TEXT, NAME, TAG NAME, CLASS NAME')

        eyes.check_region_by_selector(searchElement, value, name)

    def compare_image(self, path, imagename=None, includeEyesLog=True):
        """
        Select an image and send it to Eyes for comparison. A name can be used in place of the image's file name.

        Arguments:
                |  Path                             | Path of the image to send to eyes for visual comparison                                                               |
                |  imagename (default=None)         | Can manually set the name desired for the image passed in. If no name is passed in it will default file name of the image  |
                |  Include Eyes Log (default=True)  | The Eyes logs will be included by default. To deactivate, pass 'False' in the variable.                                    |

        Example:

        | *Keywords*         |  *Parameters*                                                                                                                       |
        | Open Browser       |  http://www.navinet.net/   |  gc                       |                            |                    |        |       |         |
        | Open Eyes Session  |  http://www.navinet.net/   |  RobotAppEyes_Test        |  NaviNet_RobotAppEyes_Test |  YourApplitoolsKey |  1024  |  768  |  False  |
        | Compare Image      |  selenium-screenshot-1.png |  Image Name Example       |                            |                    |        |       |         |
        | Close Eyes Session |                            |                           |                            |                    |        |       |         |
        """
        if imagename is None:
            tag = os.path.basename(path)
        else:
            tag = imagename

        eyes._prepare_to_check()
        if includeEyesLog is True:
            logger.set_logger(StdoutLogger())
        with open(path, 'rb') as image_file:
            screenshot64 = image_file.read().encode('base64')
        data = {'appOutput': {'title': '', 'screenshot64': screenshot64},
                'userInputs': [],
                'tag': tag,
                'ignoreMismatch': False}
        eyes._match_window_task._agent_connector.match_window(
            eyes._match_window_task._running_session, data)

    def close_eyes_session(self, includeEyesLog=True):
        """
        Closes a session and returns the results of the session.
        If a test is running, aborts it. Otherwise, does nothing.

        The RobotAppEyesTest.txt test will fail after the first run, this is because a baseline is being created and will be accepted automatically by Applitools Eyes.
        A second test run will show a successful comparison between screens and the test will pass.

        Arguments:
                |  Include Eyes Log (default=True)  | The Eyes logs will be included by default. To deactivate, pass 'False' in the variable.   |

        Example:

        | *Keywords*                    |  *Parameters*                                                                                                                      |
        | Open Browser                  |  http://www.navinet.net/  |  gc                       |                            |                    |        |       |         |
        | Open Eyes Session             |  http://www.navinet.net/  |  RobotAppEyes_Test        |  NaviNet_RobotAppEyes_Test |  YourApplitoolsKey |  1024  |  768  |  False  |
        | Check Eyes Region By Selector |  LINK TEXT                |  RESOURCES                |  NaviNetLinkTextElement    |                    |        |       |         |
        | Close Eyes Session            |                           |                           |                            |                    |        |       |         |

        """
        if includeEyesLog is True:
            logger.set_logger(StdoutLogger())

        eyes.close()
        eyes.abort_if_not_closed()

    def eyes_session_is_open(self):
        """
        Returns True if an Applitools Eyes session is currently running, otherwise it will return False.

        | *Keywords*        |  *Parameters*                                                                                                                      |
        | Open Browser      |  http://www.navinet.net/  |  gc                       |                            |                    |        |       |         |
        | Open Eyes Session |  http://www.navinet.net/  |  RobotAppEyes_Test        |  NaviNet_RobotAppEyes_Test |  YourApplitoolsKey |  1024  |  768  |  False  |
        | ${isOpen}=        |  Eyes Session Is Open     |                           |                            |                    |        |       |         |
        | Run Keyword If    |  ${isOpen}==True          | Close Eyes Session        |                            |                    |        |       |         |
        """
        return eyes.is_open()
