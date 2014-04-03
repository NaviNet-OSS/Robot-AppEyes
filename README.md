Robot-AppEyes library for Robot Framework
==================================================


Introduction
------------

Robot-AppEyes is a Robot Framework Library that uses the Python SDK [Eyes-Selenium](https://pypi.python.org/pypi/eyes-selenium) from the tool [Applitools Eyes](http://applitools.com/), providing visual verification that can be used with the [Selenium2Library](https://github.com/rtomac/robotframework-selenium2library).

The Robot-AppEyes library is the result of our initial proof of concept with the [Applitools Eyes](http://applitools.com/) tool to automate visual software testing. In order to use the Robot-AppEyes library, you are required to [sign up](https://applitools.com/sign-up/) for a free account with Applitools, further information around this can be found below in the 'Usage' section.

As new features are released by Applitools and we will endeavor to add these to this library and make them publicly available as soon as possible.

- More information about the keywords in this library can be found on the [RobotAppEyesDoc](https://github.com/NaviNet/Robot-AppEyes/doc/RobotAppEyesDoc.html) page.
- The [Eyes Selenium](https://pypi.python.org/pypi/eyes-selenium/1.15) page will provide more information for that library.
- More information about the Selenium2library can be found on the [Wiki](https://github.com/rtomac/robotframework-selenium2library/wiki) and in the [Keyword Documentation](http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html).

Requirements
------------
* Python 2.7.4 (Newer versions not tested)
* Robot Framework 2.8.3 (Newer versions not tested)
* Selenium2Library 1.5 (Newer versions not tested)
* Eyes-Selenium 1.15 (Newer versions not tested). The downloads can be found [here](https://pypi.python.org/pypi/eyes-selenium/1.15) or pip install eyes-selenium can be used.


Installation
------------
#### Using pip ####

The recommended installation method is using
[pip](http://pip-installer.org)

    pip install Robot-AppEyes

The main benefit of using ``pip`` is that it automatically installs all
dependencies needed by the library. Other useful features are easy upgrading
and support for un-installation

    pip install --upgrade Robot-AppEyes
    pip uninstall Robot-AppEyes

Notice that using ``--upgrade`` above updates both the library and all
its dependencies to the latest version. If you want, you can also install
a specific version or upgrade only the Selenium tool used by the library

    pin install Robot-AppEyes==1.0
    pip install --upgrade Robot-AppEyes
    pip install Robot-AppEyes==1.0

#### Manual installation ####

If you do not have network connection or cannot get the proxy to work, you need
to resort to manual installation. This requires installing both the library
and its dependencies yourself.

1) Make sure you have [Robot Framework installed](http://code.google.com/p/robotframework/wiki/Installation)

2) Download source distributions (``*.tar.gz`` / ``*.zip``) for the library and its
   dependencies

   - [https://pypi.python.org/pypi/Robot-AppEyes](https://pypi.python.org/pypi/Robot-AppEyes)
   - [https://pypi.python.org/pypi/eyes-selenium](https://pypi.python.org/pypi/eyes-selenium/1.15)
   - [https://pypi.python.org/pypi/robotframework-selenium2library](https://pypi.python.org/pypi/robotframework-selenium2library/1.5.0)

Eyes-selenium dependencies


   - [https://pypi.python.org/pypi/setuptools](https://pypi.python.org/pypi/setuptools)
   - [https://pypi.python.org/pypi/requests](https://pypi.python.org/pypi/requests/2.2.1)
   - [https://pypi.python.org/pypi/pypng](https://pypi.python.org/pypi/pypng/0.0.16)
   - [https://pypi.python.org/pypi/selenium](https://pypi.python.org/pypi/selenium/2.39.0)

3) Extract each source distribution to a temporary location using 7zip (or your preferred zip program).

4) Open command line and go to each directory that was created from extraction and install each project using:

       python setup.py install

Directory Layout
----------------

*RobotAppEyes/RobotAppEyes.py* :
    The Robot Python Library that makes use of the Applitools Eyes Python SDK.

*atests/RobotAppEyesTest.txt* :
    xample test file to display what various keywords from Robot-AppEyes Library accomplish

*doc/RobotAppEyesDoc.html* :
    Keyword documentation for the Robot-AppEyes library.


Usage
-----

To write tests with Robot Framework and Robot-AppEyes, 
RobotAppEyes must be imported into your Robot test suite.
See [Robot Framework User Guide](http://code.google.com/p/robotframework/wiki/UserGuide) for more information.


**Important** - You have to create a [free account](https://applitools.com/sign-up/) with Applitools in order to run the 
            Robot-AppEyes library and return results. The Applitools site will
            allow you to sign up and you will then be provide with your own API key.
            This will then need to be added to the Robot test file RoboAppEyesTest.txt,
            within the variable ${Applitools-key}, remove 'YourApplitoolsKey' and replace with your API Key.


Running the Demo
----------------

The test file RobotAppEyesTest.txt, is an easily executable test for Robot Framework using Robot-AppEyes Library. 
For in depth detail on how the keywords function, read the Keyword documentation found in *doc/RobotAppEyesDoc.html*

**Remember to include your Applitools API key otherwise the
test will not run.** To run the test navigate to the atests directory found in your C:\Python folder. Open a command prompt within the atests folder and run

    pybot RobotAppEyesTest.txt

Things to Note When Using Applitools
-----------------------------------

* The RobotAppEyesTest.txt test will fail after the first run, this is because a baseline is being created and will be accepted automatically by Applitools Eyes. A second test run will show a successful comparsion between screens and the test will pass.
* Changing the ${Applitools-AppName} variable value will create a new test entry in Applitools test result screen and a new baseline will be accepted automatically by Applitools Eyes on the first run.
* The Height resolution should not be greater than 1000, this is currently Applitools maximum setting.


Getting Help
------------
The [user group for Robot Framework](http://groups.google.com/group/robotframework-users) is the best place to get help. Include in the post:

- Full description of what you are trying to do and expected outcome
- Version number of Robot-AppEyes, Robot Framework, and Selenium2Library
- Traceback or other debug output containing error information