DJANGO_DIR="/home/itattractor/projects/zakon/www/demo/django-project/"
scp -r django-project/ itattractor@x.esdp.it-attractor.net:projects/zakon/www/demo/django-project/
ssh itattractor@x.esdp.itattractor.net cd $DJANGO_DIR | python manage.py syncdb --settings "zakon.settings_production" 
