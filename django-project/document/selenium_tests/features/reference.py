#coding=utf-8
import os
from django.core.management import call_command
from lettuce import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from django.test import LiveServerTestCase
from nose.tools import assert_equals
from document.selenium_tests.features.view_document import i_go_to_the_main_page, i_am_on_upload_page, upload_document
from zakon.settings import PROJECT_ROOT
from time import sleep
FILE_ROOT_ADRESS = os.path.join(PROJECT_ROOT, 'document/selenium_tests/features/resources/')

@step(u'я перехожу на страницу "(.*)"')
@step(u'я нахожусь на странице "(.*)"')
def i_am_on_page(step, page_name):
    i_go_to_the_main_page(step)
    elem_href = world.browser.find_element_by_link_text(page_name)
    elem_href.click()

@step(u'вижу кнопку "Ссылка" в содержании статьи-"(.*)"')
def i_see_the_add_link_button(step, article_num):
    article_content = world.browser.find_element_by_id('article_'+article_num)
    assert article_content.find_element_by_name('btn_article_'+article_num)

@step(u'я нажимаю на кнопку "Ссылка" под "(.*)"-статьей')
def i_click_the_add_link_button(step, article_num):
    button_href = world.browser.find_element_by_name('btn_article_'+article_num)
    button_href.click()

@step(u'вижу модальное окно')
def i_see_modal_form(step):
    modal_hidden_attribute = world.browser.find_element_by_id('modal').get_attribute('aria-hidden')
    assert modal_hidden_attribute == 'false'

@step(u'в модальном окне вижу ссылку "(.*)"')
def i_see_link_on_modal_form(step, link_name):
    modal_content = world.browser.find_element_by_id('accordion').text
    assert modal_content.find(link_name) != -1

@step(u'открыто модальное окно на странице "(.*)"')
def modal_form_is_opened(step, page_name):
    i_am_on_page(step, page_name)
    i_click_the_add_link_button(step, '1')

@step(u'я кликаю на ссылку "(.*)"')
def i_click_the_link(step, link_text):
    link_href = world.browser.find_element_by_partial_link_text(link_text)
    link_href.click()

@step(u'открыто окно подтверждения на странице "(.*)"')
def opened_confirm_form(step, page_name):
    i_am_on_page(step, page_name)
    i_click_the_add_link_button(step, '1')
    i_click_the_link(step, 'НАЛОГОВЫЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ')
    world.browser.find_element_by_xpath('//*[@class="accordion"]//a[text()="Статья 19. Понятие налога"]').click()

@step(u'я нажимаю на кнопку "ОК"')
def i_click_button_OK(step):
    alert = world.browser.switch_to_alert()
    alert.accept()

@step(u'вижу что нахожусь на странице "(.*)"')
def i_see_that_i_am_on_page(step, expected_title):
    title = world.browser.find_element_by_tag_name('title')
    assert_equals(title.text, expected_title)

@step(u'я добавляю ссылку с "(.*)"-статьи на "(.*)" в документе "(.*)"')
def i_add_link_to_document(step, source_article_number, target_article_name, doc_name):
    i_click_the_add_link_button(step, source_article_number)
    i_click_the_link(step, doc_name)
    world.browser.find_element_by_xpath('//*[@class="accordion"]//a[text()="'+target_article_name+'"]').click()
    i_click_button_OK(step)

@step(u'вижу что "(.*)"-статья содержит ссылку "(.*)"')
def i_see_link_in_the_content_of_article(step, article_number, link_text):
    article_content = world.browser.find_element_by_id('article_'+article_number)
    assert article_content.find_element_by_partial_link_text(link_text)



