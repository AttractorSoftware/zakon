#coding=utf-8


import os

from lettuce import step, world
from django.test import LiveServerTestCase
from nose.tools import assert_equals


from zakon.settings import PROJECT_ROOT
import time
from selenium import webdriver

FILE_ROOT_ADRESS = os.path.join(PROJECT_ROOT, '..', 'document/selenium_tests/features/')


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
        world.browser.execute_script("""alert("ysaysa;sdal");""")
        text=world.browser.find_element_by_xpath("//a[contains(text(),'ЗАКОН КЫРГЫЗСКОЙ РЕСПУБЛИКИО государственной регистрации юридическихлиц, филиалов (представительств)')]")
        time.sleep(6)
        text.click()
        time.sleep(6)
        # mouse = webdriver.ActionChains(world.browser)
        # mouse.double_click(el).perform()
        time.sleep(5)




        addButton = world.browser.find_element_by_id('ShowModalWindow')
        addButton.click()
        link_law=world.browser.find_element_by_link_text('ЗАКОН КЫРГЫЗСКОЙ РЕСПУБЛИКИ О государственной регистрации юридических лиц, филиалов (представительств)')
        link_law.click()


