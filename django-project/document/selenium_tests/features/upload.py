#coding=utf-8

import os

from lettuce import step, world
from django.test import LiveServerTestCase
from nose.tools import assert_equals

class ViewLaw(LiveServerTestCase):

    @step(u'я захожу на главную страницу')
    def i_go_to_the_main_page(step):
        world.browser.get("http://127.0.0.1:8000/home/")

    @step(u'я кликаю на ссылку "Загрузить закон"')
    def i_press(step):
        elem_href = world.browser.find_element_by_link_text("Загрузить закон")
        elem_href.click()

    @step(u'я вижу страницу с заголовком "(.*)"')
    def i_should_see(step, expected_response):

        title = world.browser.find_element_by_tag_name('title')
        assert_equals(title.text, expected_response)

    @step(u'я загружаю файл с законом в формате rtf')
    def i_upload_law(step):

        elem_browse_file = world.browser.find_element_by_id('id_doc_file')
        elem_browse_file.send_keys('~/projects/zakon/django-project/document/selenium_tests/features/zakon.rtf')
        elem_upload = world.browser.find_element_by_id('btn_upload')
        elem_upload.click()

    @step(u'производится переход на главную страницу с заголовком "(.*)"')
    def i_should_go_the_main_page(step, expected_response):

        title = world.browser.find_element_by_tag_name('title')
        assert_equals(title.text, expected_response)

    @step(u'в списке законов есть ссылка на загруженный файл')
    def i_should_go_the_main_page(step):

        elem_href = world.browser.find_element_by_xpath("/html/body/div/ol/a[1]")
        assert_equals(type(elem_href)==None, False)
