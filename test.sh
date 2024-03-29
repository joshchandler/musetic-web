#!/bin/bash

pip install -q -r requirements/test.txt

flake8 .

coverage run manage.py test
coverage report --fail-under=100
