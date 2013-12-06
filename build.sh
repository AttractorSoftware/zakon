#!/bin/sh
cd django-project
pip install -r requirements-development.txt
python manage.py harvest --tag=-skip_upload_all
nosetests tests/