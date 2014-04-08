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

from RobotAppEyes import *
from version import VERSION

_version_ = VERSION


class RobotAppEyes(RobotAppEyes):
    """
    Robot-AppEyes is a visual verfication library for Robot Framework that leverages
    the Eyes-Selenium and Selenium2 libraries. 

    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'