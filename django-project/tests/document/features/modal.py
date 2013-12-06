#coding=utf-8
import os
from lettuce import *
from tests.document.features.view_document import i_go_to_the_main_page, i_am_on_upload_page, upload_document
from zakon.settings import PROJECT_ROOT

FILE_ROOT_ADRESS = os.path.join(PROJECT_ROOT, 'document/selenium_tests/features/resources/')


def i_load_the_document(file_name):
    i_am_on_upload_page(step)
    upload_document(step, file_name)


@step(u'загружен документ ЗАКОН КЫРГЫЗСКОЙ РЕСПУБЛИКИ О государственной регистрации юридических лиц, филиалов')
def i_load_the_document_zakon(step):
    i_load_the_document('zakon.rtf')


@step(u'загружен документ НАЛОГОВЫЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ')
def i_load_the_document_Nalogovij_Kodeks(step):
    i_load_the_document('Nalogovij_Kodeks.rtf')


@step(u'я нахожусь на странице "(.*)"')
def i_am_on_page(step, page_name):
    i_go_to_the_main_page(step)
    elem_href = world.browser.find_element_by_link_text(page_name)
    elem_href.click()


@step(u'вижу кнопку "Ссылка" в содержании статьи-"(.*)"')
def i_see_the_add_link_button(step, article_num):
    article_content = world.browser.find_element_by_id('article_' + article_num)
    assert article_content.find_element_by_name('btn_article_' + article_num)


@step(u'я нажимаю на кнопку "Ссылка" под "(.*)"-статьей')
def i_click_the_add_link_button(step, article_num):
    button_href = world.browser.find_element_by_name('btn_article_' + article_num)
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


@step(u'вижу следующие статьи в контенте документа "(.*)":')
def i_see_next_articles(step, page_name):
    i_click_the_link(step, page_name)
    for link_dictionary in step.hashes:
        world.browser.find_element_by_xpath('//*[@id="accordion"]//a[normalize-space(text())="'+page_name+'"]/../../div[2]//a[text()="'+link_dictionary['article_name']+'"]')

@step(u'вижу статью "(.*)" в контенте документа "(.*)"')
def i_see_article_in_content_of_document(step, article_name, law_name):
    world.browser.find_element_by_xpath('//*[@id="accordion"]//a[normalize-space(text())="'+law_name+'"]/../../div[2]//a[text()="'+article_name+'"]')

@step(u'вижу следующие статьи в модальном окне')
def i_see_next_links_on_modal_form(step):
    for link_dictionary in step.hashes:
        i_click_the_link(step, link_dictionary['law_name'])
        world.browser.find_element_by_xpath('//*[@id="accordion"]//a[normalize-space(text())="'+link_dictionary['law_name']+'"]/../../div[2]//a[text()="'+link_dictionary['article_name']+'"]')
