cd django-project
pip install -r requirements-development.txt
python manage.py harvest
nosetests document/tests/