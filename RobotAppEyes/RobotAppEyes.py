#!/usr/bin/env python


#  Copyright 2013-2014 NaviNet Inc.
# 
#  Thomas Armstrong, Simon McMorran, Gareth Nixon and Adam Simmons
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
import robot
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidElementStateException
from robot.libraries.BuiltIn import BuiltIn
from applitools import logger
from applitools.logger import StdoutLogger
from applitools import geometry
from applitools.geometry import Region
from applitools.eyes import Eyes
from applitools import _webdriver
from applitools._webdriver import EyesWebDriver
from Selenium2Library.keywords import _browsermanagement




class RobotAppEyes:
    """
    Robot-AppEyes is a visual verfication library for Robot Framework that leverages
    the Eyes-Selenium and Selenium2 libraries. 
    
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'



    def open_eyes_session(self, url, appname, testname, apikey, width=None, height=None):
        """
        Starts a session with the Applitools Eyes Website.

        Arguments:
                |  URL (string)              | The URL to start the test on               |
                |  Application Name (string) | The name of the application under test.    |
                |  Test Name (string)        | The test name.                             |
                |  API Key (string)          | User's Applitools Eyes key.                |
                |  (Optional) Width (int)    | The width of the browser window e.g. 1280  |
                |  (Optional) Height (int)   | The height of the browser window e.g. 1000 |


        Creates an instance of the Selenium2Library webdriver.
        Defines a global driver and sets the Selenium2Library webdriver to the global driver.

        Checks if there has been a width or height value passed in. 
        If there no are values passed in, eyes calls the method open without the width and height values.
        Otherwise eyes calls open with the width and height values defined.

        The driver then gets the url that will be tested.

        Example:

        | Open Browser       |  ${TestURL}          | gc         |              |          |            |             |
        | Open Eyes Session  |  ${TestURL}          | ${AppName} |  ${testname} |  ${key}  |  ${width}  |  ${height}  |
        | Check Eyes Window  |  ${ElementTagName}   |            |              |          |            |             |
        | Close Eyes Session |                      |            |              |          |            |             |   

        """

        Eyes.api_key = apikey
        s2l = BuiltIn().get_library_instance('Selenium2Library')
        webdriver = s2l._current_browser()
        global driver
        driver = webdriver
        global eyes   
        eyes = Eyes()
        logger.set_logger(StdoutLogger())

        if width==None and height==None:
            eyes.open(driver, appname, testname)
        else:   
            intwidth= int(width)
            intheight= int(height)
            eyes.open(driver, appname, testname, {'width': intwidth, 'height': intheight})
            driver.get(url)

    def check_eyes_window(self, name):
        """
        Takes a snapshot from the browser using the web driver and matches it with
        the expected output.

        Arguments:
                |  Name (string)     | The region tag name.  |

        Example:

        | Open Browser       |  ${TestURL}          | gc         |              |          |            |             |
        | Open Eyes Session  |  ${TestURL}          | ${AppName} |  ${testname} |  ${key}  |  ${width}  |  ${height}  |
        | Check Eyes Window  |  ${ElementTagName}   |            |              |          |            |             |
        | Close Eyes Session |                      |            |              |          |            |             | 

        """
        logger.set_logger(StdoutLogger())

        eyes.check_window(name)

    def check_eyes_region(self, element, width, height, name):
        """
        Takes a snapshot of the given region from the browser using the web driver to locate an xpath element
        with a certain width and height and matches it with the expected output. 
        The width and the height cannot be greater than the width and the height specified in the open_eyes_session keyword.

        Arguments:
                |  Element (string)  | This needs to be passed in as an xpath e.g. //*[@id="navbar"]/div/div   |
                |  Width (int)       | The width of the region that is tested e.g. 500                         |
                |  Height (int)      | The height of the region that is tested e.g. 120                        |
                |  Name (string)     | The region tag name.                                                    |
        
        Example:

        | Open Browser       |  ${TestURL}      | gc               |                    |                       |            |             |
        | Open Eyes Session  |  ${TestURL}      | ${AppName}       |  ${testname}       |  ${key}               |  ${width}  |  ${height}  |
        | Check Eyes Region  |  ${ElementXpath} | ${ElementWidth}  |  ${ElementHeight}  |  ${ElementTagName}    |            |             |
        | Close Eyes Session |                  |                  |                    |                       |            |             |
        
        """
        logger.set_logger(StdoutLogger())

        intwidth= int(width)
        intheight= int(height)

        searchElement = driver.find_element_by_xpath(element)
        location = searchElement.location
        region = Region(location["x"], location["y"], intwidth, intheight)
        eyes.check_region(region, name)

    def check_eyes_region_by_element(self, selector, value, name):
        """
        Takes a snapshot of the region of the given selector and element value from the browser using the web driver
        and matches it with the expected output. With a choice from four selectors, listed below to check by. 

        Arguments:
                |  Selector (string) | This will decide what element will be located. The supported selectors include: xpath, id, class and css     |
                |  Value (string)    | The specific value of the selector. e.g. an xpath value //*[@id="navbar"]/div/div                            |
                |  Name (string)     | The region tag name.                                                                                         |
        
        Example:

        | Open Browser                  |  ${TestURL}           |  gc               |                    |          |            |             |
        | Open Eyes Session             |  ${TestURL}           |  ${AppName}       |  ${testname}       |  ${key}  |  ${width}  |  ${height}  |
        | Check Eyes Region By Element  |  ${ElementSelector}   |  ${ElementValue}  |  ${ElementTagName} |          |            |             |
        | Close Eyes Session            |                       |                   |                    |          |            |             |

        """
        logger.set_logger(StdoutLogger())

        searchElement = None

        if selector in ('Xpath', 'xpath', 'XPATH'):
            searchElement = driver.find_element_by_xpath(value)
        elif selector in ('Id', 'id', 'ID'):
            searchElement = driver.find_element_by_id(value)
        elif selector in ('Class', 'class', 'CLASS'):
            searchElement = driver.find_element_by_class_name(value)
        elif selector in ('Css', 'css', 'CSS'):
            searchElement = driver.find_element_by_css_selector(value)
        else:
            raise InvalidElementStateException('Please select a valid selector: xpath, id, class or css')
        eyes.check_region_by_element(searchElement, name)


    def close_eyes_session(self): 
        """
        Closes a session and returns the results of the session.
        If a test is running, aborts it. Otherwise, does nothing.
        """
        logger.set_logger(StdoutLogger())

        eyes.close()
        eyes.abort_if_not_closed()