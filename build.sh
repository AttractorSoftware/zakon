#!/bin/sh
cd django-project
pip install -r requirements-development.txt
python manage.py test -v 2 --jenkins
python manage.py harvest --tag=-skip_upload_all --with-xunit --xunit-file=reports/lettuce.xml
