#coding=utf-8
from tests.document.features.view_document import *

FILE_ROOT_ADRESS = os.path.join(PROJECT_ROOT, 'tests/resources/')

@step(u'вижу сообщение "(.*)"')
def i_see_message(step, message_text):
     found_message = world.browser.find_element_by_xpath('//h2[1]')
     assert_equals(message_text, found_message.text)

@step(u'вижу ошибку с текстом "(.*)"')
def i_see_error_text(step, error_text):
   found_error = world.browser.find_element_by_xpath('//*/li/p[text()]')
   assert_equals(error_text, found_error.text)

@step(u'вижу страницу с заголовком "(.*)"')
def i_see_page_with_header(step, expected_title):
    check_the_header(expected_title)

@step(u'вижу текст "(.*)" вместо имени закона')
def i_see_error_text_instead_of_the_name(step, header_name):
    check_the_header(header_name)

@step(u'вижу текст "(.*)" вместо даты и места принятия закона')
def i_dont_see_name_of_law(step, error_text):
    found_text = world.browser.find_element_by_xpath('//*[@id="list"]/div/p[@id="place"]')
    assert_equals(found_text.text.strip(), error_text)

@step(u'вижу текст "(.*)" вместо ревизии закона')
def i_dont_see_name_of_law(step, error_text):
    found_text = world.browser.find_element_by_xpath('//*[@id="list"]/div/p[@id="revisions"]')
    assert_equals(found_text.text.strip(), error_text)

@step(u'я нахожусь на странице с найденными ошибками в документе "(.*)"')
def i_have_error_page(step, law_name):
    i_am_on_upload_page(step)
    upload_document(step, law_name)


@step(u'нажимаю "(.*)"')
def i_push_upload_button(step, submit_upload):
    found_button = world.browser.find_element_by_xpath('//*[@value="'+submit_upload+'"]')
    found_button.click()

@step(u'вижу документ загруженный с ошибками "(.*)"')
def i_see_unnamed_document(step, expected_response):
    i_see_document_link(step, expected_response)


@step(u'нажимаю на кнопку "Отменить"')
def i_push_cancel_button(step):
    found_button = world.browser.find_element_by_xpath('//form/button')
    found_button.click()
    wait_for()

@step(u'я загрузил документ "(.*)" с ошибками')
def i_load_the_document_with_errors(step, file_name):
    i_am_on_upload_page(step)
    upload_document(step, file_name)
    i_push_upload_button(step, 'Загрузить с ошибками')

@step(u'вижу документ загруженный с ошибками:')
def i_see_uploaded_document_with_errors(step):
    law_link_text = step.multiline.replace('\n', " ")
    world.browser.find_element_by_link_text(law_link_text)

