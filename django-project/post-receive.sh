#!/bin/sh

DEMO_DIR="../../www/demo/django-project/"
VIRT_ENV_DIR="../../www/virt/bin/activate"

source $VIRT_ENV_DIR
cd $DEMO_DIR
git pull
pip install -r requirements-production.txt
python manage.py syncdb