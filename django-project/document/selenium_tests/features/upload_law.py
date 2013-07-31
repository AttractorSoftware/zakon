#coding=utf-8
from lettuce import step, world
from django.test import LiveServerTestCase
from nose.tools import assert_equals
from view_law import ViewLaw

class UploadLaw(LiveServerTestCase):
    @step(u'я нахожусь на странице загрузки закона')
    def i_stay_on_the_upload_page(step):
        world.browser.get("http://127.0.0.1:8000/upload/")

    @step(u'я загружаю файл "zakon.rtf"')
    def i_upload(step):

        elem_browse_file = world.browser.find_element_by_id('id_doc_file')
        elem_browse_file.send_keys('~/projects/zakon/django-project/document/selenium_tests/features/zakon.rtf')
        elem_upload = world.browser.find_element_by_id('btn_upload')
        elem_upload.click()

    @step(u'вижу главную страницу с заголовком "(.*)"')
    def i_upload(step, expected_title):

        title = world.browser.find_element_by_tag_name('title')
        assert_equals(title.text, expected_title)

    @step(u'в списке законов вижу ссылку "(.*)"')
    def i_should_see_the_link_to_uploaded_law(step, expected_link_text):

        elem_href = world.browser.find_element_by_link_text(expected_link_text)
        assert_equals(type(elem_href)==None, False)

