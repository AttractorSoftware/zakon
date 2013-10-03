#coding=utf-8
import os
from lettuce import *
from django.test import LiveServerTestCase
from nose.tools import assert_equals
from zakon.settings import PROJECT_ROOT
FILE_ROOT_ADRESS = os.path.join(PROJECT_ROOT, '..','document/selenium_tests/features/')


@step(u'я нахожусь на странице загрузки документа')
def i_am_on_upload_page(step):
    world.browser.get("http://127.0.0.1:8000/upload/")

@step(u'загружаю документ "(.*)"')
def upload_document(step, expected_file_name):
    elem_browse_file = world.browser.find_element_by_id('id_doc_file')
    elem_browse_file.send_keys(FILE_ROOT_ADRESS+expected_file_name)
    elem_upload = world.browser.find_element_by_id('btn_upload')
    elem_upload.click()

@step(u'вижу, что нахожусь на главной странице')
def on_main_page_assert(step):
    assert_equals("http://127.0.0.1:8000/", world.browser.current_url)

@step(u'вижу ссылку "(.*)"')
def i_see_link(step, expected_response):
    elem_href = world.browser.find_element_by_link_text(expected_response)
    assert_equals(elem_href.text, expected_response)

@step(u'я загрузил документ "(.*)"')
def i_have_uploaded_document(step, doc_name):
    i_am_on_upload_page(step)
    upload_document(step, doc_name)


@step(u'нахожусь на главной странице')
def i_go_to_the_main_page(step):
    world.browser.get("http://127.0.0.1:8000/")

@step(u'вижу страницу с заголовком "(.*)"')
def i_should_see_the_link_to_uploaded_law(step, expected_title):
    title = world.browser.find_element_by_tag_name('title')
    assert_equals(title.text, expected_title)

@step(u'в списке загруженных законов есть ссылка на "(.*)"')
def i_should_see_the_link_text(step, expected_link_text):
    uploaded_law_link = world.browser.find_element_by_link_text(expected_link_text)
    assert_equals(type(uploaded_law_link)==None, False)

@step(u'я кликаю на ссылку "(.*)"')
def i_should_see_the_link_to_uploaded_law(step, expected_response):
    elem_href = world.browser.find_element_by_link_text(expected_response)
    elem_href.click()
