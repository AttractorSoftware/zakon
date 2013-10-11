#coding=utf-8


import os

from lettuce import step, world
from django.test import LiveServerTestCase
from nose.tools import assert_equals
from selenium.webdriver import ActionChains

from zakon.settings import PROJECT_ROOT
import time
from selenium import webdriver

FILE_ROOT_ADRESS = os.path.join(PROJECT_ROOT, 'document/selenium_tests/features/')


class ReferenceLaw(LiveServerTestCase):
    @step(u'имеются загруженные законы "(.*)" и "(.*)" с заголовками "(.*)" и "(.*)"')
    def i_go_to_the_main_page(step, first_law, second_loaw, first_title, second_title):
        step.given(u'я нахожусь на странице загрузки закона')
        step.given(u'я загружаю файл "{law}"'.format(law=first_law))
        step.given(u'в списке законов вижу ссылку "{title}"'.format(title=first_title))
        # step.given(u'я кликаю на ссылку "{title}"'.format(title=first_title))
        # step.given(u'вижу страницу с заголовком "{title}"'.format(title=first_title))

        step.given(u'я нахожусь на странице загрузки закона')
        step.given(u'я загружаю файл "{law}"'.format(law=second_loaw))
        step.given(u'в списке законов вижу ссылку "{title}"'.format(title=second_title))
        # step.given(u'я кликаю на ссылку "{title}"'.format(title=second_title))
        # step.given(u'вижу страницу с заголовком "{title}"'.format(title=second_title))


    @step(u'я перехожу по ссылке "(.*)"')
    def i_go_to_the_law_page(step, name_of_law):
        step.given(u'я нахожусь на главной странице')
        step.given(u'я кликаю на ссылку "{title}"'.format(title=name_of_law))

    @step(u'я нахожу текст "(.*)" и выделяю его')
    def i_select_text(step, name_of_law):
        el = world.browser.find_element_by_id('article4_item_2')

        ActionChains(world.browser).click_and_hold(el).move_to_element_with_offset(el,30,0).perform()



