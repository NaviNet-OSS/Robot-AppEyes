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

import sys
from distutils.core import setup
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'RobotAppEyes'))

execfile(join(dirname(__file__), 'RobotAppEyes', 'version.py'))

DESCRIPTION = """
Robot-AppEyes is a visual verfication library for Robot Framework
that leverages the Eyes-Selenium and Selenium2 libraries.
"""[1:-1]

setup(name              = 'Robot-AppEyes',
      version           = VERSION,
      description       = 'Visual Verification testing library for Robot Framework',
      long_description  = DESCRIPTION,
      author            = 'Thomas Armstrong, Simon McMorran, Gareth Nixon, Adam Simmons',
      author_email      = '<tarmstrong@navinet.net>, <smcmorran@navinet.net>, <gnixon@navinet.net>, <asimmons@navinet.net>',
      url               = 'https://github.com/NaviNet/Robot-AppEyes',
      license           = 'Apache License 2.0',
      keywords          = 'robotframework testing testautomation eyes-selenium selenium2 visual-verification',
      platforms         = 'any',
      classifiers       = [
                              "License :: OSI Approved :: Apache Software License",
                              "Programming Language :: Python",
                              "Development Status :: 4 - Beta",
                              "Intended Audience :: Developers",
                              "Programming Language :: Python :: 2.7",
                              "Topic :: Software Development :: Testing",
                              "Topic :: Software Development :: Quality Assurance"
                        ],
      install_requires  = [
							'robotframework >= 2.8.4',
							'robotframework-selenium2library >= 1.5.0',
							'eyes-selenium >= 1.31'
				],
      packages          = ['RobotAppEyes'],
      data_files        = [('Tests', ['Tests/acceptance/RobotAppEyesTest.txt', 'Tests/acceptance/1.png', 'Tests/acceptance/2.png', 'doc/RobotAppEyes-KeywordDocumentation.html', 'doc/ChangeLog.txt'])],
      download_url      = 'https://github.com/NaviNet/Robot-AppEyes/tarball/1.1',
      )