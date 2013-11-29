# -*- coding: UTF-8 -*-
from unittest import TestCase
from document.law_parser.builder import Builder


class Test_UploadDocument_WithError(TestCase):
    def test_build_name_with_incorrect_text_must_raise_error(self):
        builder = Builder(
            u'Закон закон неправильный закон\n'
            u'Нету имени закона'
            )
        error = []
        result = builder.build_revisions()
        self.assertEqual(u'Не найдены ревизии закона', result)
        error.append(result)

        result =builder.errors
        self.assertEqual(error, result)

    def test_build_place_and_date_with_incorrect_text_must_raise_error(self):
        builder = Builder(
            u'Закон закон неправильный закон\n'
            u'Нету место и дата принятие закона'
            )
        error = []
        result = builder.build_revisions()
        self.assertEqual(u'Не найдены ревизии закона', result)
        error.append(result)

        result =builder.errors
        self.assertEqual(error,result)

    def test_build_revision_with_incorrect_text_must_raise_error(self):
        builder = Builder(
            u'Закон закон неправильный закон\n'
            u'Нету ревизии закона'
            )

        error = []
        result = builder.build_revisions()
        self.assertEqual(u'Не найдены ревизии закона', result)
        error.append(result)

        result =builder.errors
        self.assertEqual(error,result)

    def test_build_errors_with_incorrect_text_must_raise_error(self):
        builder = Builder(
            u'Закон закон неправильный закон\n'
            u'Документ неправильно оформлен'
            )

        error = []
        error_msg = u'Не найдены место и дата принятия'
        error.append(error_msg)
        error_msg = u'Не найдено наименование закона'
        error.append(error_msg)
        error_msg = u'Не найдены ревизии закона'
        error.append(error_msg)

        builder.build_place_and_date()
        builder.build_name()
        builder.build_revisions()
        result =builder.errors

        self.assertEqual(error,result)

