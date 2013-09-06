#coding=utf-8

import os

from lettuce import step, world
from django.test import LiveServerTestCase
from nose.tools import assert_equals

class ViewLaw(LiveServerTestCase):

    @step(u'я нахожусь на главной странице')
    def i_go_to_the_main_page(step):
        world.browser.get("http://127.0.0.1:8000/")

    @step(u'в списке загруженных законов есть ссылка на "(.*)"')
    def i_should_see_the_link_text(step, expected_link_text):
        uploaded_law_link = world.browser.find_element_by_link_text(expected_link_text)
        assert_equals(type(uploaded_law_link)==None, False)

    @step(u'я кликаю на ссылку "(.*)"')
    def i_should_see_the_link_to_uploaded_law(step, expected_response):

        elem_href = world.browser.find_element_by_link_text(expected_response)
        elem_href.click()

    @step(u'вижу страницу с заголовком "(.*)"')
    def i_should_see_the_link_to_uploaded_law(step, expected_title):
        title = world.browser.find_element_by_tag_name('title')
        assert_equals(title.text, expected_title)