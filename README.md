# CSEC380Project
![Build Status](https://travis-ci.org/ioannidisa/CSEC380Project.svg?branch=master)

A fake video sharing platform with some awesome security vulnerabilities.

## To Run
To execute a version of the site, execute the script `build-run.sh` and visit
the site by going to `http://localhost:4000` You must have docker installed.

## To Run Tests
To run the tests, perform the run operation above and then execute the following command:
`docker exec python ./manage.py test app`