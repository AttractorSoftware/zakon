#coding=utf-8
from os import walk
from lettuce import *

docsUploadedWithErrorCount = 0


@step(u'я нахожусь на странице загрузки документа')
def i_am_on_upload_page(step):
    world.browser.get("http://127.0.0.1:8000/upload/")


@step(u'я загрузил все документы из каталога "(.*?)"')
def i_have_uploaded_document(step, docs_dir):
    global docsUploadedWithErrorCount
    filePaths = []
    for (dirpath, dirnames, filenames) in walk(docs_dir):
        filePaths.extend(filenames)
        break
    for filePath in filePaths:
        filePath = docs_dir + filePath
        print u'загружаю документ "' + filePath + '"'
        i_am_on_upload_page(step)
        upload_document(step, filePath)

    allDocsCount = str(len(filePaths))
    docsUploadedWithoutErrorCount = str(len(filePaths) - docsUploadedWithErrorCount)
    docsUploadedWithErrorCount = str(docsUploadedWithErrorCount)
    print u"Количество всех документов: " + allDocsCount + "\r\n" + \
          u"Количество загруженных без ошибок: " + docsUploadedWithErrorCount + "\r\n" + \
          u"Количество загруженных с ошибками: " + docsUploadedWithoutErrorCount + "\r\n"


def upload_document(step, expected_file_name):
    global docsUploadedWithErrorCount
    elem_browse_file = world.browser.find_element_by_id('id_doc_file')
    elem_browse_file.send_keys(expected_file_name)
    elem_upload = world.browser.find_element_by_id('btn_upload')
    elem_upload.click()

    world.browser.implicitly_wait(0)
    try:
        world.browser.find_element_by_id('upload_anyway_button').click()
    except Exception:
        docsUploadedWithErrorCount += 1