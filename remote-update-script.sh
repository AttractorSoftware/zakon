#!/bin/sh

VIRT_ENV_DIR="/home/itattractor/.virtualenvs/zakon-env/bin/activate"
DEMO_DIR='projects/zakon/www/demo/django-project'
SETTINGS="zakon.settings_production"


cd ${DEMO_DIR}
git pull
source ${VIRT_ENV_DIR}
pip install -r requirements-production.txt
python manage.py syncdb --settings ${SETTINGS}