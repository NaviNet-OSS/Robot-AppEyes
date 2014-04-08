#!/usr/bin/env python

import sys
from distutils.core import setup
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'RobotAppEyes'))

execfile(join(dirname(__file__), 'RobotAppEyes', 'version.py'))

DESCRIPTION = """
Robot-AppEyes is a visual verfication library for Robot Framework
that leverages the Eyes-Selenium and Selenium2 libraries.
"""[1:-1]

setup(name              = 'RobotAppEyes',
      version           = VERSION,
      description       = 'Visual Verification testing library for Robot Framework',
      long_description  = DESCRIPTION,
      author            = 'Thomas Armstrong, Simon McMorran, Gareth Nixon, Adam Simmons',
      author_email      = '<tehtom@hotmail.co.uk>, <sijm007@gmail.com>, <gnixon@navinet.net>, <asimmons@navinet.net>',
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
							'robotframework >= 2.8.3',
							'robotframework-selenium2library >= 1.5.0',
							'eyes-selenium >= 1.15'
				],
      packages          = ['RobotAppEyes'],
      data_files        = [('atests', ['atests/RobotAppEyesTest.txt', 'doc/RobotAppEyesDoc.html'])],
      download_url      = 'https://github.com/NaviNet/Robot-AppEyes/tarball/1.0',
      )