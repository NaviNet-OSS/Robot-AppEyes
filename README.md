Robot-AppEyes library for Robot Framework
==================================================


Introduction
------------

Robot-AppEyes is a Robot Framework Library to automate visual software testing verification. Robot-AppEyes uses a Python SDK called [Eyes-Selenium](https://pypi.python.org/pypi/eyes-selenium) from the tool [Applitools Eyes](http://applitools.com/), and can be used with the [Selenium2Library](https://github.com/rtomac/robotframework-selenium2library).

The Robot-AppEyes library is the result of our work with [Applitools Eyes](http://applitools.com/). In order to use the Robot-AppEyes library, you are required to [sign up](https://applitools.com/sign-up/) for a free account with Applitools. See the [Usage](https://github.com/NaviNet/Robot-AppEyes#usage) section.

- Information about Robot-AppEyes keywords can be found on the [RobotAppEyes-Keyword Documentation](http://navinet.github.io/Robot-AppEyes/RobotAppEyes-KeywordDocumentation.html) page.
- The [Eyes Selenium](https://pypi.python.org/pypi/eyes-selenium/2.5) page provides more information for that library.
- More information about the Selenium2library can be found on the [Selenium2Library Wiki](https://github.com/rtomac/robotframework-selenium2library/wiki) and in the [Keyword Documentation](http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html).

Requirements
------------
* Python 2.7.4 (Newer versions not tested)
* Robot Framework 2.8.7 (Newer versions not tested)
* Selenium2Library 1.7.4 (Newer versions not tested)
* Eyes-Selenium 3.2 (Newer versions not tested)


Installation
------------
#### Using pip ####

The recommended installation tool is [pip](http://pip-installer.org).

Install pip.
Enter the following:

    pip install Robot-AppEyes

Append ``--upgrade`` to update both the library and all 
its dependencies to the latest version:

    pip install --upgrade Robot-AppEyes

To install a specific version enter:

    pip install Robot-AppEyes==(DesiredVersion)

#### Manual Installation ####
It is also possible to install the package with python, though you will need dependencies to be installed manually.
you can download the source distribution from PyPI, extract it and 
run the following command:

    python setup.py install

Alternatively you could download the source code, package it and install using next commands:

        python setup.py sdist
        pip install resulting_package
        ## dist/robot-appEyes-1.2.zip        

#### Uninstall ####

To uninstall Robot-AppEyes use the following pip command: 

    pip uninstall Robot-AppEyes

However, if the package was installed manually it will need to be uninstalled manually:

1) Navigate to ``C:\Python27\Tests`` and delete RobotAppEyesTest.txt, pictureOne.png, pictureTwo.png and RobotAppEyes-KeywordDocumentation.html

2) Navigate to ``C:\Python27\Lib\site-packages`` and delete RobotAppEyes-1.2-py2.7.egg-info and the folder ``RobotAppEyes``

Directory Layout
----------------

*RobotAppEyes/RobotAppEyes.py* :
    The Robot Python Library that makes use of the Applitools Eyes Python SDK.

*Tests/acceptance/RobotAppEyesTest.txt* :
    Example test file to display what various keywords from Robot-AppEyes Library accomplish

*doc/RobotAppEyes-KeywordDocumentation.html* :
    Keyword documentation for the Robot-AppEyes library.


Usage
-----

To write tests with Robot Framework and Robot-AppEyes, 
RobotAppEyes must be imported into your Robot test suite.
See [Robot Framework User Guide](http://code.google.com/p/robotframework/wiki/UserGuide) for more information.


**Note** - You must create a [free account](https://applitools.com/sign-up/) with Applitools in order to run the 
            Robot-AppEyes library and return results. The Applitools site will
            allow you to sign up and you will then be provide with your own API key.
            This will then need to be added to the Robot test file RoboAppEyesTest.txt,
            within the variable ${Applitools-Key}, remove 'YourApplitoolsKey' and replace with your API Key.


Running the Demo
----------------

The test file RobotAppEyesTest.txt, is an easily executable test for Robot Framework using Robot-AppEyes Library. 
For in depth detail on how the keywords function, read the Keyword documentation found here : [Keyword Documentation](http://navinet.github.io/Robot-AppEyes/RobotAppEyes-KeywordDocumentation.html)

**Remember to include your Applitools API key otherwise the
test will not run.** To run the test navigate to the Tests directory in C:\Python folder. Open a command prompt within the *Tests/acceptance* folder and run:

    pybot RobotAppEyesTest.txt

**Note:** It is assumed that anyone who wants to use this demo script is already able to execute robot tests using Google Chrome.

To view a failed comparison between two images, run the test with 1.png in the Compare Image keyword. Next, replace the file name pictureOne.png with pictureTwo.png in the RobotAppEyesTest script and exectue tests again.


Things to Note When Using Applitools
-----------------------------------

* The RobotAppEyesTest.txt test will fail after the first run because a baseline is being created and will be accepted automatically by Applitools Eyes. A second test run will show a successful comparison between screens and the test will pass.
* Changing the ${Applitools-AppName} variable value will create a new test entry in Applitools test result screen and a new baseline will be accepted automatically by Applitools Eyes on the first run.
* The Height resolution should not be greater than 1000 which is currently Applitools maximum setting.
* Browser zoom should be set to 100%.


Getting Help
------------
The [user group for Robot Framework](http://groups.google.com/group/robotframework-users) is the best place to get help. Include in the post:

- Full description of what you are trying to do and expected outcome
- Version number of Robot-AppEyes, Robot Framework, and Selenium2Library
- Traceback or other debug output containing error information