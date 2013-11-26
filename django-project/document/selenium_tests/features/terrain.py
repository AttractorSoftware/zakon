from django.conf import settings
from django.db import connection
from lettuce import before, after, world
from selenium import webdriver
from django.core.management import call_command
@before.all
def initial_setup():
    connection.creation.destroy_test_db(settings.DATABASES['default']['NAME'])
    call_command('syncdb', interactive=False, verbosity=1)
    world.browser = webdriver.Firefox()
    world.browser.implicitly_wait(10)

@after.all
def teardown_browser(total):
    connection.creation.destroy_test_db(settings.DATABASES['default']['NAME'])
    call_command('syncdb', interactive=False, verbosity=1)
    world.browser.quit()

@after.each_feature
def after_feature(feature):
    call_command('flush', interactive=False, verbosity=1)