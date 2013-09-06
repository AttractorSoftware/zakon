
from lettuce import before, after, world
from selenium import webdriver

@before.all
def initial_setup():
    world.browser = webdriver.Firefox()

@after.all
def teardown_browser(total):
    world.browser.quit()
