#coding=utf-8
import os
import re
from lettuce import *
from selenium.webdriver.common.action_chains import ActionChains
from django.test import LiveServerTestCase
from nose.tools import assert_equals
from zakon.settings import PROJECT_ROOT
from time import sleep

FILE_ROOT_ADRESS = os.path.join(PROJECT_ROOT, 'document/selenium_tests/features/resources/')


@step(u'я нахожусь на странице загрузки документа')
def i_am_on_upload_page(step):
    world.browser.get("http://127.0.0.1:8000/upload/")


@step(u'загружаю документ "(.*)"')
def upload_document(step, expected_file_name):
    elem_browse_file = world.browser.find_element_by_id('id_doc_file')
    elem_browse_file.send_keys(FILE_ROOT_ADRESS + expected_file_name)
    elem_upload = world.browser.find_element_by_id('btn_upload')
    elem_upload.click()


@step(u'вижу, что нахожусь на главной странице')
def on_main_page_assert(step):
    assert_equals("http://127.0.0.1:8000/", world.browser.current_url)


@step(u'вижу ссылку "(.*)"')
def i_see_document_link(step, expected_response):
    i_see_link(expected_response)


@step(u'я загрузил документ "(.*)"$')
def i_have_uploaded_document(step, doc_name):
    i_am_on_upload_page(step)
    upload_document(step, doc_name)


@step(u'нахожусь на главной странице')
def i_go_to_the_main_page(step):
    world.browser.get("http://127.0.0.1:8000/")


@step(u'я кликаю на ссылку "(.*)"')
def i_should_see_the_link_to_uploaded_law(step, expected_response):
    elem_href = world.browser.find_element_by_link_text(expected_response)
    elem_href.click()


@step(u'вижу страницу с заголовком "(.*)"')
def i_should_see_the_link_to_uploaded_law(step, expected_title):
    title = world.browser.find_element_by_tag_name('title')
    assert_equals(title.text, expected_title)


@step(u'я нахожусь на странице с заголовком "(.*)"')
def im_on_law_page(step, expected_response):
    i_am_on_upload_page(step)
    upload_document(step, "zakon.rtf")
    navigate_to_page(expected_response)


@step(u'внутри "(.*)" кликаю по кнопке "(.*)"')
def press_button_in(step, section, button_name):
    button = world.browser.find_element_by_xpath(
        '//*/h3[text()="' + section + '"]/following-sibling::div[1]/a[text()="' + button_name + '"]')
    button.click()


@step(u'вижу модальное окно со списком статей')
def i_see_modal_window(step):
    world.browser.find_element_by_xpath("//form[@class='modal hide in']")


@step(u'расскрываю документ "(.*)"')
def i_expand_window(step, doc_name):
    expand_collapse_list(doc_name)


@step(u'вижу окно подтверждения')
def i_see_alert(step):
    alert = world.browser.switch_to_alert()
    assert_equals(u'Вы хотите добавить ссылку?', alert.text)


@step(u'я кликаю "ОК')
def i_click_ok(step):
    alert = world.browser.switch_to_alert()
    alert.accept()


@step(u'вижу что нахожусь в документе "(.*)"')
def i_see_me_in_document(step, doc_name):
    check_the_header(doc_name)


@step(u'вижу ссылку с текстом "(.*)"')
def i_see_link(step, expected_response):
    world.browser.find_element_by_link_text(expected_response)


@step(u'загружен документ "(.*)"')
def document_uploaded(step, doc_name):
    _upload_document(doc_name)


@step(u'нахожусь на странице документа "(.*)"')
def on_page(step, page_name):
    navigate_to_page(page_name)


@step(u'вижу модальное окно "(.*)"')
def see_modal_window(step, modal_name):
    modal_window_header = world.browser.find_element_by_xpath("//form[@class='modal hide in']/div/h2")
    assert_equals(modal_name, modal_window_header.text)


@step(u'в документе "(.*)" вижу статью "(.*)"')
def see_in_document_list(step, doc_name, article_name):
    expand_collapse_list(doc_name)
    world.modal_window = world.browser.find_element_by_xpath(
        '//form[@class="modal hide in"]/div/div[2]/div[2]/div[1]/a[normalize-space(text())="' + doc_name + '"]')
    world.modal_window.find_element_by_xpath('../..').find_element_by_link_text(article_name)


@step(u'щелкаю на ссылку "(.*)"')
def click_the_article_link(step, article_name):
    article_link = world.modal_window.find_element_by_xpath('../..//a[normalize-space(text())="' + article_name + '"]')
    article_link.click()


@step(u'вижу ссылку "(.*)" под статьей "(.*)"')
def i_see_link_under_section(step, link_text, section):
    article_element = world.browser.find_element_by_xpath(
        '//*/h3[text()="' + section + '"]/following-sibling::div[1]//a[text()="' + link_text + '"]')
    assert_equals(link_text, article_element.text)


@step(u'вижу комментарий к "(.*)"-главе с текстом "(.*)"')
def i_see_comment_to_chapter(step, chapter_number, expected_comment):
    comment = world.browser.find_element_by_xpath('//div[@id="chapter_'+chapter_number+'"]/div[@class="comment"]/h4').text
    assert_equals(expected_comment, comment.replace('\n', " "))


@step(u'вижу комментарий к "(.*)"-статье с текстом "(.*)"')
def i_see_comment_to_article(step, article_number, expected_comment):
    comment = world.browser.find_element_by_xpath('//div[@id="article_'+article_number+'"]').text
    assert_equals(expected_comment, comment.replace('\n', " ")[7:])



@step(u'вижу описание к заголовку "(.*)" с текстом "(.*)"')
def i_see_description_to_header(step, doc_name, description_text):
    world.browser.find_element_by_xpath('//*[@id="list"]/div/h1[text()="'+doc_name+'"]/following-sibling::p[contains(text(),"'+description_text+'")]')


def navigate_to_page(expected_response):
    elem_href = world.browser.find_element_by_link_text(expected_response)
    elem_href.click()


def _upload_document(doc_name):
    i_am_on_upload_page(step)
    upload_document(step, doc_name)


def click_the_link(header_name):
    document_name = world.browser.find_element_by_link_text(header_name)
    document_name.click()


def i_see_link(header_name):
    elem_href = world.browser.find_element_by_link_text(header_name)
    assert_equals(elem_href.text.strip(), header_name)


def expand_collapse_list(list_name):
    list = world.browser.find_element_by_link_text(list_name)
    list.click()


def check_the_header(header_name):
    found_header = world.browser.find_element_by_xpath('//*[@id="list"]/div/h1')
    assert_equals(header_name, re.sub(r"\n{1,}", r" ", found_header.text))


def wait_for():
    world.browser.implicitly_wait(20)

