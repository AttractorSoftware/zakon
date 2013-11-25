#coding=utf-8
import os
from os import walk
from lettuce import *
from zakon.settings import PROJECT_ROOT

FILE_ROOT_ADDRESS = os.path.join(PROJECT_ROOT, 'document/selenium_tests/features/resources/')


@step(u'я нахожусь на странице загрузки документа')
def i_am_on_upload_page(step):
    world.browser.get("http://127.0.0.1:8000/upload/")


@step(u'я загружаю все документы из каталога resources')
def i_have_uploaded_document(step):
    f = []
    for (dirpath, dirnames, filenames) in walk(FILE_ROOT_ADDRESS):
        f.extend(filenames)
        break
    for filePath in f:
        filePath = FILE_ROOT_ADDRESS + filePath
        i_am_on_upload_page(step)
        upload_document(step, filePath)

@step(u'загружаю документ')
def upload_document(step, expected_file_name):
    elem_browse_file = world.browser.find_element_by_id('id_doc_file')
    elem_browse_file.send_keys(expected_file_name)
    elem_upload = world.browser.find_element_by_id('btn_upload')
    elem_upload.click()

    try:
        upload_anyway_button = world.browser.find_element_by_id('upload_anyway_button')
    except Exception as e:
        upload_anyway_button = 0
    if upload_anyway_button != 0:
        upload_anyway_button.click()