#!/bin/sh
export FLASK_APP=./user_manager/index.py
pipenv run flask --debug run -h 0.0.0.0