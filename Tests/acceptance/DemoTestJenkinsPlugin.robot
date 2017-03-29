*** Settings ***
Library                                             Selenium2Library
Library                                             RobotAppEyes

*** Variables ***
### Selenium2Library Variables ###
${Timeout}                                          15

### Css Variables ###
${Features}                                         css=.features>a

### Applitools Variables ###
${Applitools-url}                                   https://www.applitools.com/
${Applitools-AppName}                               MyAppName
${Applitools-TestName}                              MyTestName
${Applitools-Key}                                   YOUR_API_KEY
${Width}                                            1000
${Height}                                           800
${MatchLevel}                                       LAYOUT2
${True}                                             True
${False}                                            False
${firstBatchName}                                   MyBatchName
${matchTimeout}                                     3000

*** Test Cases ***

Test1
    [Documentation]
    Open Browser                                    ${Applitools-url}       Chrome
    Open Eyes Session                               appname=${Applitools-AppName}    testname=${Applitools-TestName}     apikey=${Applitools-Key}      width=${Width}      height=${Height}         matchlevel=${MatchLevel}        batchName=${firstBatchName}     ApplitoolsJenkinsPlugin=${True}        fullPageScreenshot=${False}     hideScrollBar=${True}       matchTimeout=${matchTimeout}
    Check Eyes Window                               Main Page New
    Close Browser
    Close Eyes Session
