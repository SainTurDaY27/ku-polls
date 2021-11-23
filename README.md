# ku-polls
<!-- [![Build Status](https://travis-ci.com/SainTurDaY27/ku-polls.svg?branch=My-repository-in-SKE)](https://travis-ci.com/SainTurDaY27/ku-polls)  -->
[![Build Status](https://app.travis-ci.com/SainTurDaY27/ku-polls.svg?branch=My-repository-in-SKE)](https://app.travis-ci.com/SainTurDaY27/ku-polls)
[![codecov](https://codecov.io/gh/SainTurDaY27/ku-polls/branch/My-repository-in-SKE/graph/badge.svg?token=WMCFGLGB5L)](https://codecov.io/gh/SainTurDaY27/ku-polls)

A web application for conducting polls at [Kasetsart University](https://www.ku.ac.th)

## [Project Documents]

[Project Wiki](../../wiki/Home)  
[Background](../../wiki/Background)  
[Vision Statement](../../wiki/Vision%20Statement)  
[Requirements](../../wiki/Requirements)

## Running KU Polls

Users provided by the initial data (users.json):

| Username  | Password    |
|-----------|-------------|
| demo1     | Vote4me!    |
| demo2     | Vote4me2    |

## Install application
python3 manage.py migrate  
python3 manage.py loaddata users polls
