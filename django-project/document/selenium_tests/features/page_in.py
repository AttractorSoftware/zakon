#coding=utf-8

from lettuce import step, world, before
#from django.db import connection
#from django.conf import settings

from selenium import webdriver
from django.test import LiveServerTestCase
from nose.tools import assert_equals
from django.core.management import call_command
from lettuce import before, after, world


@before.all
def initial_setup():
    call_command('syncdb', interactive=False, verbosity=1)
    world.browser = webdriver.Firefox()

@after.all
def teardown_browser(total):
    #connection.creation.destroy_test_db(settings.DATABASES['default']['NAME'])
    world.browser.quit()



class PageIn(LiveServerTestCase):

    @step(u'I go to the main page') # here we go to the main page
    def i_go_to_the_main_page(step):
        world.browser.get("http://127.0.0.1:8000/home/")

    @step(u'I press any link')  # here wy search any link in list and click on it
    def i_press(step):
        elem_href = world.browser.find_element_by_xpath("/html/body/div/ol/a[1]") # find first link and click on it
        elem_href.click()

    @step(u'I should see page with title "(.*)"')   # here we see document and analyze title of it
    def i_should_see(step, expected_response):

        title = world.browser.find_element_by_tag_name('title')
        assert_equals(title.text, expected_response)














