source `which virtualenvwrapper.sh`
cd django-project
workon zakon-env
pip install -r requirements-development.txt
python manage.py harvest
nosetests document/tests/**/*