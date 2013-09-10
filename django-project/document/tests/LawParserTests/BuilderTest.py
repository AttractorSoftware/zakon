#coding=utf-8
from unittest import TestCase
from document.LawParser.Builder import Builder, ParserError
from document.LawParser.elements.section import Section
from document.LawParser.elements.text_section import TextSection


class BuilderTest(TestCase):

    def test_build_name_in_one_line(self):
        builder = Builder(
            u'г.Бишкек\n'\
            u'от 17 октября 2008 года N 230\n'\
            u'\n'\
            u'НАЛОГОВЫЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ\n'\
            u'(Вводится в действие Законом Кыргызской Республики\n'\
            u'от 17 октября 2008 года N 231)')

        self.assertEqual(u'НАЛОГОВЫЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ', builder.build_name())

        builder.text = \
            u'г.Бишкек\n'\
            u'от 5 января 1998 года N 1\n'\
            u'\n'\
            u'ГРАЖДАНСКИЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ\n'\
            u'\n'\
            u'(В редакции Законов КР от\n'

        self.assertEqual(u'ГРАЖДАНСКИЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ', builder.build_name())

    def test_build_name_in_multiple_line(self):
        builder = Builder(
            u'г.Бишкек\n'\
            u'от 20 февраля 2009 года N 57\n'\
            u'\n'\
            u'ЗАКОН КЫРГЫЗСКОЙ РЕСПУБЛИКИ\n'\
            u'\n'\
            u'О государственной регистрации юридических\n'\
            u'лиц, филиалов (представительств)\n'\
            u'\n'\
            u'(В редакции Законов КР от 15 июля 2009 года N 207,')

        self.assertEqual(
            u'ЗАКОН КЫРГЫЗСКОЙ РЕСПУБЛИКИ\n'\
            u'\n'\
            u'О государственной регистрации юридических\n'\
            u'лиц, филиалов (представительств)', builder.build_name())

    def test_build_revisions(self):
        builder = Builder(
            u'(представительств)\n'\
            u'\n'\
            u'(В редакции Законов КР от 15 июля 2009 года N 207,\n'\
            u'18 декабря 2009 года N 313, 21 декабря 2011 года N 241,\n'\
            u'13 апреля 2012 года N 35, 13 декабря 2012 года N 199)\n'\
            u'\n'\
            u'Статья 1.')

        self.assertEqual(
            u'(В редакции Законов КР от 15 июля 2009 года N 207,\n'\
            u'18 декабря 2009 года N 313, 21 декабря 2011 года N 241,\n'\
            u'13 апреля 2012 года N 35, 13 декабря 2012 года N 199)', builder.build_revisions())

    def test_build_place_and_date(self):
        builder = Builder(
            u'г.Бишкек\n'\
            u'от 17 октября 2008 года N 230\n'\
            u'\n'\
            u'НАЛОГОВЫЙ')

        self.assertEqual(u"""г.Бишкек
от 17 октября 2008 года N 230""", builder.build_place_and_date())

    def test_build_name_with_incorrect_text_must_raise_error(self):
        builder = Builder(
            u'Закон закон неправильный закон\n'
            u'Нету имени закона'
        )

        try:
            result = builder.build_name()
        except ParserError as ex:
            result = 'exception handled'

        self.assertEqual('exception handled', result)
        self.assertTrue(isinstance(ex, ParserError))
        self.assertEqual(u'Не найдено наименование закона', ex[0])

    def test_build_revisions_with_incorrect_text_must_raise_error(self):
        builder = Builder(
            u'Закон закон неправильный закон\n'
            u'Нету ревизий закона'
        )

        try:
            result = builder.build_revisions()
        except ParserError as ex:
            result = 'exception handled'

        self.assertEqual('exception handled', result)
        self.assertTrue(isinstance(ex, ParserError))
        self.assertEqual(u'Не найдены ревизии закона', ex[0])

    def test_build_place_and_date_with_incorrect_text_must_raise_error(self):
        builder = Builder(
            u'Закон закон неправильный закон\n'
            u'Нету ревизий закона'
        )

        try:
            result = builder.build_place_and_date()
        except ParserError as ex:
            result = 'exception handled'

        self.assertEqual('exception handled', result)
        self.assertTrue(isinstance(ex, ParserError))
        self.assertEqual(u'Не найдены место и дата принятия', ex[0])

    def test_build_articles_with_items(self):
        builder = Builder(
            u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
            u'Республики\n'\
                u'\n'\
                u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                u'2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.\n'\
                u'3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...\n'\
                u'\n'\
            u'Статья 2. Налоговое законодательство Кыргызской Республики\n'\
                u'\n'\
                u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                u'3. Настоящий Кодекс устанавливает:...\n'\
                u'\n'
            u'Статья 3. Действие международных договоров и иных соглашений\n'\
                u'\n'\
                u'1. Если вступившим в установленном законом порядке международным договором, участником...\n'\
                u'2. Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...')
        expected_articles = []

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        expected_articles.append(article)

        article = TextSection(level='article', name=u'Статья 2. Налоговое законодательство Кыргызской Республики', number='2')

        item = TextSection(level='article2_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        expected_articles.append(article)

        article = TextSection(level='article', name=u'Статья 3. Действие международных договоров и иных соглашений', number='3')

        item = TextSection(level='article3_item', name='', number='1')
        item.text = u'Если вступившим в установленном законом порядке международным договором, участником...'
        article.add_section(item)

        item = TextSection(level='article3_item', name='', number='2')
        item.text = u'Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
        article.add_section(item)

        expected_articles.append(article)

        self.assertEqual(expected_articles, builder.build_sections())

    def test_build_articles_with_text_content(self):
        builder = Builder(
            u'Статья 2. Государственный орган, осуществляющий регистрацию\n'\
                u'\n'\
                u'Уполномоченный государственный орган, осуществляющий регистрацию юридических лиц...\n'\
                u'\n'\
            u'Статья 3. Цели регистрации\n'
                u'\n'\
                u'Регистрация осуществляется в целях:\n'\
                u'- удостоверения факта создания, внесения изменений и дополнений в государственный реестр, а также...\n'\
                u'- учета зарегистрированных (перерегистрированных) и прекративших деятельность юридических лиц, филиалов (представительств);\n'\
                u'- ведения государственного реестра;\n'\
                u'- предоставления заинтересованным физическим и юридическим лицам информации о зарегистрированных (перерегистрированных)...'
        )

        expected_articles = []

        article = TextSection('article', '2', u'Статья 2. Государственный орган, осуществляющий регистрацию')
        article.text = u'Уполномоченный государственный орган, осуществляющий регистрацию юридических лиц...'

        expected_articles.append(article)

        article = TextSection('article', '3', u'Статья 3. Цели регистрации')
        article.text = \
            u'Регистрация осуществляется в целях:\n'\
            u'- удостоверения факта создания, внесения изменений и дополнений в государственный реестр, а также...\n'\
            u'- учета зарегистрированных (перерегистрированных) и прекративших деятельность юридических лиц, филиалов (представительств);\n'\
            u'- ведения государственного реестра;\n'\
            u'- предоставления заинтересованным физическим и юридическим лицам информации о зарегистрированных (перерегистрированных)...'

        expected_articles.append(article)

        self.assertEqual(expected_articles, builder.build_sections())

    def test_build_chapters_with_articles(self):
        builder = Builder(
            u'Глава 1\n'\
            u'Общие положения\n'\
                '\n'\
                u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
                u'Республики\n'\
                    u'\n'\
                    u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                    u'2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.\n'\
                    u'3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...\n'\
                    u'\n'\
                u'Статья 2. Налоговое законодательство Кыргызской Республики\n'\
                    u'\n'\
                    u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                    u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                    u'3. Настоящий Кодекс устанавливает:...\n'\
                    u'\n'
                u'Статья 3. Действие международных договоров и иных соглашений\n'\
                    u'\n'\
                    u'1. Если вступившим в установленном законом порядке международным договором, участником...\n'\
                    u'2. Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
                    u'\n'\
            u'Глава 2\n'\
            u'Налоговая система Кыргызской Республики\n'\
                '\n'\
                u'Статья 4. Государственный орган, осуществляющий регистрацию\n'\
                    u'\n'\
                    u'Уполномоченный государственный орган, осуществляющий регистрацию юридических лиц...\n'\
                    u'\n'\
                u'Статья 5. Цели регистрации\n'
                    u'\n'\
                    u'Регистрация осуществляется в целях:\n'\
                    u'- удостоверения факта создания, внесения изменений и дополнений в государственный реестр, а также...\n'\
                    u'- учета зарегистрированных (перерегистрированных) и прекративших деятельность юридических лиц, филиалов (представительств);\n'\
                    u'- ведения государственного реестра;\n'\
                    u'- предоставления заинтересованным физическим и юридическим лицам информации о зарегистрированных (перерегистрированных)...'
        )

        expected_chapters = []

        chapter = Section('chapter', name= u'Глава 1 Общие положения', number='1')

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        chapter.add_section(article)

        article = TextSection(level='article', name=u'Статья 2. Налоговое законодательство Кыргызской Республики', number='2')

        item = TextSection(level='article2_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        chapter.add_section(article)

        article = TextSection(level='article', name=u'Статья 3. Действие международных договоров и иных соглашений', number='3')

        item = TextSection(level='article3_item', name='', number='1')
        item.text = u'Если вступившим в установленном законом порядке международным договором, участником...'
        article.add_section(item)

        item = TextSection(level='article3_item', name='', number='2')
        item.text = u'Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
        article.add_section(item)

        chapter.add_section(article)

        expected_chapters.append(chapter)

        chapter = Section('chapter', name= u'Глава 2 Налоговая система Кыргызской Республики', number='2')

        article = TextSection('article', '4', u'Статья 4. Государственный орган, осуществляющий регистрацию')
        article.text = u'Уполномоченный государственный орган, осуществляющий регистрацию юридических лиц...'

        chapter.add_section(article)

        article = TextSection('article', '5', u'Статья 5. Цели регистрации')
        article.text = \
            u'Регистрация осуществляется в целях:\n'\
            u'- удостоверения факта создания, внесения изменений и дополнений в государственный реестр, а также...\n'\
            u'- учета зарегистрированных (перерегистрированных) и прекративших деятельность юридических лиц, филиалов (представительств);\n'\
            u'- ведения государственного реестра;\n'\
            u'- предоставления заинтересованным физическим и юридическим лицам информации о зарегистрированных (перерегистрированных)...'

        chapter.add_section(article)

        expected_chapters.append(chapter)

        actual_chapters = builder.build_sections()
        self.assertEqual(expected_chapters, actual_chapters)

    def test_build_chapter_with_paragraphs(self):
        builder = Builder(
            u'Глава 1\n'\
            u'Общие положения\n'\
                u'\n'\
                u'Параграф 1\n'\
                u'Общие положения о купле-продаже\n'\
                    u'\n'\
                    u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
                    u'Республики\n'\
                        u'\n'\
                        u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                        u'2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.\n'\
                        u'3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...\n'\
                        u'\n'\
                    u'Статья 2. Налоговое законодательство Кыргызской Республики\n'\
                        u'\n'\
                        u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                        u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                        u'3. Настоящий Кодекс устанавливает:...\n'\
                        u'\n'
                    u'Статья 3. Действие международных договоров и иных соглашений\n'\
                        u'\n'\
                        u'1. Если вступившим в установленном законом порядке международным договором, участником...\n'\
                        u'2. Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
                        u'\n'\
                u'Параграф 2\n'\
                u'Розничная купля-продажа\n'\
                    u'\n'\
                    u'Статья 4. Государственный орган, осуществляющий регистрацию\n'\
                        u'\n'\
                        u'Уполномоченный государственный орган, осуществляющий регистрацию юридических лиц...\n'\
                        u'\n'\
                    u'Статья 5. Цели регистрации\n'
                        u'\n'\
                        u'Регистрация осуществляется в целях:\n'\
                        u'- удостоверения факта создания, внесения изменений и дополнений в государственный реестр, а также...\n'\
                        u'- учета зарегистрированных (перерегистрированных) и прекративших деятельность юридических лиц, филиалов (представительств);\n'\
                        u'- ведения государственного реестра;\n'\
                        u'- предоставления заинтересованным физическим и юридическим лицам информации о зарегистрированных (перерегистрированных)...'
        )

        chapter = Section('chapter', name= u'Глава 1 Общие положения', number='1')

        paragraph = Section('chapter1_paragraph', u'Параграф 1 Общие положения о купле-продаже', '1')

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        paragraph.add_section(article)

        article = TextSection(level='article', name=u'Статья 2. Налоговое законодательство Кыргызской Республики', number='2')

        item = TextSection(level='article2_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        paragraph.add_section(article)

        article = TextSection(level='article', name=u'Статья 3. Действие международных договоров и иных соглашений', number='3')

        item = TextSection(level='article3_item', name='', number='1')
        item.text = u'Если вступившим в установленном законом порядке международным договором, участником...'
        article.add_section(item)

        item = TextSection(level='article3_item', name='', number='2')
        item.text = u'Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
        article.add_section(item)

        paragraph.add_section(article)

        chapter.add_section(paragraph)

        paragraph = Section('chapter1_paragraph', u'Параграф 2 Розничная купля-продажа', '2')

        article = TextSection('article', name=u'Статья 4. Государственный орган, осуществляющий регистрацию', number='4')
        article.text = u'Уполномоченный государственный орган, осуществляющий регистрацию юридических лиц...'

        paragraph.add_section(article)

        article = TextSection('article', name=u'Статья 5. Цели регистрации', number= '5')
        article.text = \
            u'Регистрация осуществляется в целях:\n'\
            u'- удостоверения факта создания, внесения изменений и дополнений в государственный реестр, а также...\n'\
            u'- учета зарегистрированных (перерегистрированных) и прекративших деятельность юридических лиц, филиалов (представительств);\n'\
            u'- ведения государственного реестра;\n'\
            u'- предоставления заинтересованным физическим и юридическим лицам информации о зарегистрированных (перерегистрированных)...'

        paragraph.add_section(article)

        chapter.add_section(paragraph)

        expected_chapters = []

        expected_chapters.append(chapter)

        actual_chapters = builder.build_sections()
        self.assertEqual(expected_chapters, actual_chapters)

    def test_build_division_with_chapters(self):
        builder = Builder(
            u'РАЗДЕЛ I\n'\
            u'ОБЩИЕ ПОЛОЖЕНИЯ\n'\
            '\n' \
                u'Глава 1\n' \
                u'Общие положения\n'\
                    u'\n'\
                    u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
                    u'Республики\n'\
                        u'\n'\
                        u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                        u'2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.\n'\
                        u'3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...\n'\
                        u'\n'\
                    u'Статья 2. Налоговое законодательство Кыргызской Республики\n'\
                        u'\n'\
                        u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                        u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                        u'3. Настоящий Кодекс устанавливает:...\n'\
                        u'\n'
                    u'Статья 3. Действие международных договоров и иных соглашений\n'\
                        u'\n'\
                        u'1. Если вступившим в установленном законом порядке международным договором, участником...\n'\
                        u'2. Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
                        u'\n'\
        )

        expected_divisions = []

        division = Section('division', name= u'РАЗДЕЛ I ОБЩИЕ ПОЛОЖЕНИЯ', number='I')

        chapter = Section('chapter', name= u'Глава 1 Общие положения', number='1')

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        chapter.add_section(article)

        article = TextSection(level='article', name=u'Статья 2. Налоговое законодательство Кыргызской Республики', number='2')

        item = TextSection(level='article2_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        chapter.add_section(article)

        article = TextSection(level='article', name=u'Статья 3. Действие международных договоров и иных соглашений', number='3')

        item = TextSection(level='article3_item', name='', number='1')
        item.text = u'Если вступившим в установленном законом порядке международным договором, участником...'
        article.add_section(item)

        item = TextSection(level='article3_item', name='', number='2')
        item.text = u'Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
        article.add_section(item)

        chapter.add_section(article)

        division.add_section(chapter)

        expected_divisions.append(division)

        self.assertEqual(expected_divisions, builder.build_sections())

    def test_build_divisions_with_sub_divisions(self):
        builder = Builder(
            u'РАЗДЕЛ I\n'\
            u'ОБЩИЕ ПОЛОЖЕНИЯ\n'\
            '\n'\
                u'Подраздел 1. я подраздел 1\n'\
                '\n'\
                u'Глава 1\n' \
                u'Общие положения\n'\
                    u'\n'\
                    u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
                    u'Республики\n'\
                        u'\n'\
                        u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                        u'2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.\n'\
                        u'3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...\n'\
                        u'\n'\
            u'Подраздел 2. я подраздел 2\n'
                u'Глава 2\n'\
                u'Налоговая система Кыргызской Республики\n'\
                    '\n'\
                    u'Статья 4. Государственный орган, осуществляющий регистрацию\n'\
                        u'\n'\
                        u'Уполномоченный государственный орган, осуществляющий регистрацию юридических лиц...\n'\
                        u'\n'\
        )

        expected_divisions = []

        division = Section('division', name= u'РАЗДЕЛ I ОБЩИЕ ПОЛОЖЕНИЯ', number='I')

        sub_division = Section('divisionI_sub_division', name=u'Подраздел 1. я подраздел 1', number='1')

        chapter = Section('chapter', name= u'Глава 1 Общие положения', number='1')

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        chapter.add_section(article)
        sub_division.add_section(chapter)
        division.add_section(sub_division)

        sub_division = Section('divisionI_sub_division', name=u'Подраздел 2. я подраздел 2', number='2')

        chapter = Section('chapter', name= u'Глава 2 Налоговая система Кыргызской Республики', number='2')

        article = TextSection('article', '4', u'Статья 4. Государственный орган, осуществляющий регистрацию')
        article.text = u'Уполномоченный государственный орган, осуществляющий регистрацию юридических лиц...'

        chapter.add_section(article)

        sub_division.add_section(chapter)

        division.add_section(sub_division)

        expected_divisions.append(division)

        self.assertEqual(expected_divisions, builder.build_sections())

    def test_build_parts(self):
        builder = Builder(
            u'ОБЩАЯ ЧАСТЬ\n'\
                '\n' \
                u'РАЗДЕЛ I\n'\
                u'ОБЩИЕ ПОЛОЖЕНИЯ\n'\
                '\n' \
                    u'Глава 1\n' \
                    u'Общие положения\n'\
                        u'\n'\
                        u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
                        u'Республики\n'\
                            u'\n'\
                            u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                            u'\n'\
            u'ОСОБЕННАЯ ЧАСТЬ\n'\
                '\n' \
                u'РАЗДЕЛ I\n'\
                u'ОБЩИЕ ПОЛОЖЕНИЯ\n'\
                '\n' \
                    u'Глава 1\n' \
                    u'Общие положения\n'\
                        u'\n'\
                        u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
                        u'Республики\n'\
                            u'\n'\
                            u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                            u'\n'\
        )

        expected_parts = []

        part = Section('part', name=u'ОБЩАЯ ЧАСТЬ', number='1')
        division = Section('division', name= u'РАЗДЕЛ I ОБЩИЕ ПОЛОЖЕНИЯ', number='I')
        chapter = Section('chapter', name= u'Глава 1 Общие положения', number='1')

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        chapter.add_section(article)
        division.add_section(chapter)
        part.add_section(division)

        expected_parts.append(part)

        part = Section('part', name=u'ОСОБЕННАЯ ЧАСТЬ', number='2')
        division = Section('division', name= u'РАЗДЕЛ I ОБЩИЕ ПОЛОЖЕНИЯ', number='I')
        chapter = Section('chapter', name= u'Глава 1 Общие положения', number='1')

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        chapter.add_section(article)
        division.add_section(chapter)
        part.add_section(division)

        expected_parts.append(part)

        actual_parts = builder.build_sections()
        self.assertEqual(expected_parts, actual_parts)

    def test_build_empty_sections_must_raise_error(self):
        builder = Builder(
            u'Статья 2. Государственный орган, осуществляющий регистрацию\n'\
            u'\n'\
            u'Статья 3. Цели регистрации\n'
            u'\n'\
        )

        try:
            result = builder.build_sections()
        except ParserError as ex:
            result = 'exception handled'

        self.assertEqual('exception handled', result)
        self.assertTrue(isinstance(ex, ParserError))
        self.assertEqual(u'Ошиибка! "Статья 2. Государственный орган, осуществляющий регистрацию" не имеет содержимого!', ex[0])

        builder.text = \
            u'Глава 1\n'\
            u'Общие положения\n'\
                '\n'\

        try:
            result = builder.build_sections()
        except ParserError as ex:
            result = 'exception handled'
        self.assertEqual('exception handled', result)
        self.assertTrue(isinstance(ex, ParserError))
        self.assertEqual(u'Ошиибка! "Глава 1 Общие положения" не имеет содержимого!', ex[0])

        builder.text = \
            u'Подраздел 1. Я подраздел 1\n'\
                '\n'\

        try:
            result = builder.build_sub_divisions(0, len(builder.text), '')
        except ParserError as ex:
            result = 'exception handled'
        self.assertEqual('exception handled', result)
        self.assertTrue(isinstance(ex, ParserError))
        self.assertEqual(u'Ошиибка! "Подраздел 1. Я подраздел 1" не имеет содержимого!', ex[0])

        builder.text = \
            u'РАЗДЕЛ I ОБЩИЕ ПОЛОЖЕНИЕ\n'\
                '\n'\

        try:
            result = builder.build_sections()
        except ParserError as ex:
            result = 'exception handled'
        self.assertEqual('exception handled', result)
        self.assertTrue(isinstance(ex, ParserError))
        self.assertEqual(u'Ошиибка! "РАЗДЕЛ I ОБЩИЕ ПОЛОЖЕНИЕ" не имеет содержимого!', ex[0])

        builder.text = \
            u'Подраздел 1. Я подраздел 1\n'\
                '\n'\

        try:
            result = builder.build_sub_divisions(0, len(builder.text), '')
        except ParserError as ex:
            result = 'exception handled'
        self.assertEqual('exception handled', result)
        self.assertTrue(isinstance(ex, ParserError))
        self.assertEqual(u'Ошиибка! "Подраздел 1. Я подраздел 1" не имеет содержимого!', ex[0])

        builder.text = \
            u'ОБЩАЯ ЧАСТЬ\n'\
                '\n'\

        try:
            result = builder.build_sections()
        except ParserError as ex:
            result = 'exception handled'
        self.assertEqual('exception handled', result)
        self.assertTrue(isinstance(ex, ParserError))
        self.assertEqual(u'Ошиибка! "ОБЩАЯ ЧАСТЬ" не имеет содержимого!', ex[0])

    def test_builder_must_ignore_contents_if_it_exist(self):
        """Builder должен находить верхний структурный элемент. Здесь это ЧАСТЬ II.
        И начать строить объекты с последнего совпадения с заголовком "ЧАСТЬ II".
        Все что до игнорируется"""
        builder = Builder(
        u'г.Бишкек\n'\
        u'от 5 января 1998 года N 1\n'\
        u'\n'\
        u'ГРАЖДАНСКИЙ КОДЕКС КЫРГЫЗСКОЙ РЕСПУБЛИКИ\n'\
        u'\n'\
        u'(тут редакции и все такое.\n'\
        u'ЧАСТЬ II.\n'\
            u'РАЗДЕЛ IV. ОТДЕЛЬНЫЕ ВИДЫ ОБЯЗАТЕЛЬСТВ\n'\
                u'Глава 23. Купля-продажа\n'\
                    u'Параграф 1. Общие положения о купле-продаже\n'\
                    u'Параграф 2. Розничная купля-продажа\n'\
                    u'Параграф 3. Поставка товаров\n'\
                    u'Параграф 4. Энергоснабжение\n'\
                    u'Параграф 5. Продажа предприятия. и т.д.\n'\
                    u'\n'\
                    u'А вот то что нужно:\n'\
                    u'\n'\
        u'ЧАСТЬ II\n'\
            u'\n'\
            u'РАЗДЕЛ IV\n'\
            u'ОТДЕЛЬНЫЕ ВИДЫ ОБЯЗАТЕЛЬСТВ\n'\
                u'\n'\
                u'Глава 23\n'\
                u'Купля-продажа\n'\
                u'\n'\
                    u'Параграф 1\n'\
                    u'Общие положения о купле-продаже\n'\
                        u'\n'\
                        u'Статья 415. Договор купли-продажи\n'\
                        u'\n'\
                        u'текст статьи\n'\
        )
        actual_parts = builder.build_sections()
        article = TextSection(u'article', '415', u'Статья 415. Договор купли-продажи')
        article.text = u'текст статьи'
        paragraph = Section('chapter23_paragraph', u'Параграф 1 Общие положения о купле-продаже', "1")
        paragraph.add_section(article)
        chapter = Section('chapter', u'Глава 23 Купля-продажа', "23")
        chapter.add_section(paragraph)
        division = Section('division', u'РАЗДЕЛ IV ОТДЕЛЬНЫЕ ВИДЫ ОБЯЗАТЕЛЬСТВ', 'IV')
        division.add_section(chapter)
        part = Section('part', u'ЧАСТЬ II', '1')
        part.add_section(division)
        expected_parts = []
        expected_parts.append(part)

        self.assertEqual(expected_parts, actual_parts)

    def test_build_articles_with_combine_number_via_hyphen(self):
        builder = Builder(
            u'Статья 1-1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
            u'Республики\n'\
                u'\n'\
                u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                u'2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.\n'\
                u'3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...\n'\
                u'\n'\
            u'Статья 2-156. Налоговое законодательство Кыргызской Республики\n'\
                u'\n'\
                u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                u'3. Настоящий Кодекс устанавливает:...\n'\
                u'\n'
            u'Статья 3-34586. Действие международных договоров и иных соглашений\n'\
                u'\n'\
                u'1. Если вступившим в установленном законом порядке международным договором, участником...\n'\
                u'2. Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...')
        expected_articles = []

        article = TextSection(level='article', name=u'Статья 1-1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1-1')

        item = TextSection(level='article1-1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1-1_item', name='', number='2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1-1_item', name='', number='3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        expected_articles.append(article)

        article = TextSection(level='article', name=u'Статья 2-156. Налоговое законодательство Кыргызской Республики', number='2-156')

        item = TextSection(level='article2-156_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2-156_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2-156_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        expected_articles.append(article)

        article = TextSection(level='article', name=u'Статья 3-34586. Действие международных договоров и иных соглашений', number='3-34586')

        item = TextSection(level='article3-34586_item', name='', number='1')
        item.text = u'Если вступившим в установленном законом порядке международным договором, участником...'
        article.add_section(item)

        item = TextSection(level='article3-34586_item', name='', number='2')
        item.text = u'Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
        article.add_section(item)

        expected_articles.append(article)
        actual_articles = builder.build_sections()
        self.assertEqual(expected_articles, actual_articles)

    def test_build_chapter_with_combine_number_via_hyphen(self):
        builder = Builder(
            u'Глава 1-1\n'\
            u'Общие положения\n'\
                u'\n'\
                u'Статья 2-1. Налоговое законодательство Кыргызской Республики\n'\
                    u'\n'\
                    u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                    u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                    u'3. Настоящий Кодекс устанавливает:...\n'\
                    u'\n'
        )

        expected_sections = []

        chapter = Section('chapter', name=u'Глава 1-1 Общие положения', number='1-1')

        article = TextSection(level='article', name=u'Статья 2-1. Налоговое законодательство Кыргызской Республики', number='2-1')

        item = TextSection(level='article2-1_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2-1_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2-1_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        chapter.add_section(article)

        expected_sections.append(chapter)

        actual_sections = builder.build_sections()
        self.assertEqual(expected_sections, actual_sections)

    def test_build_chapter_and_with_combine_number_via_hyphen_include_paragraphs(self):
        builder = Builder(
            u'Глава 1-1\n'\
            u'Общие положения\n'\
                u'\n'\
                u'Параграф 1-1. я параграф с комбо-номером\n'\
                u'\n'\
                u'Статья 2-1. Налоговое законодательство Кыргызской Республики\n'\
                    u'\n'\
                    u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                    u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                    u'3. Настоящий Кодекс устанавливает:...\n'\
                    u'\n'
        )

        expected_sections = []

        chapter = Section('chapter', name=u'Глава 1-1 Общие положения', number='1-1')

        paragraph = Section('chapter1-1_paragraph', name=u'Параграф 1-1. я параграф с комбо-номером', number='1-1')

        article = TextSection(level='article', name=u'Статья 2-1. Налоговое законодательство Кыргызской Республики', number='2-1')

        item = TextSection(level='article2-1_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2-1_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2-1_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        paragraph.add_section(article)
        chapter.add_section(paragraph)

        expected_sections.append(chapter)

        actual_sections = builder.build_sections()
        self.assertEqual(expected_sections, actual_sections)

    def test_build_chapter_with_article_in_one_level(self):
        builder = Builder(
            u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
            u'Республики\n'\
                u'\n'\
                u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                u'2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.\n'\
                u'3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...\n'\
                u'\n'\
            u'Глава 1\n'\
            u'Общие положения\n'\
                u'\n'\
                u'Статья 2. Налоговое законодательство Кыргызской Республики\n'\
                    u'\n'\
                    u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                    u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                    u'3. Настоящий Кодекс устанавливает:...\n'\
                    u'\n'
        )

        expected_sections = []

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        expected_sections.append(article)

        chapter = Section('chapter', name=u'Глава 1 Общие положения', number='1')

        article = TextSection(level='article', name=u'Статья 2. Налоговое законодательство Кыргызской Республики', number='2')

        item = TextSection(level='article2_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        chapter.add_section(article)

        expected_sections.append(chapter)

        actual_sections = builder.build_sections()
        self.assertEqual(expected_sections, actual_sections)

    def test_build_division_with_articles(self):
        builder = Builder(
            u'РАЗДЕЛ I\n'\
            u'ОБЩИЕ ПОЛОЖЕНИЯ\n'\
                u'\n'\
                u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
                u'Республики\n'\
                    u'\n'\
                    u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                    u'2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.\n'\
                    u'3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...\n'\
                    u'\n'\
                u'Статья 2. Налоговое законодательство Кыргызской Республики\n'\
                    u'\n'\
                    u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                    u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                    u'3. Настоящий Кодекс устанавливает:...\n'\
                    u'\n'
        )

        expected_sections = []

        division = Section('division', name= u'РАЗДЕЛ I ОБЩИЕ ПОЛОЖЕНИЯ', number='I')

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        division.add_section(article)

        article = TextSection(level='article', name=u'Статья 2. Налоговое законодательство Кыргызской Республики', number='2')

        item = TextSection(level='article2_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        division.add_section(article)

        expected_sections.append(division)

        actual_sections = builder.build_sections()

        self.assertEqual(expected_sections, actual_sections)

    def test_build_division_with_chapter_and_article_in_one_level(self):
        builder = Builder(
            u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
            u'Республики\n'\
                u'\n'\
                u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                u'2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.\n'\
                u'3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...\n'\
                u'\n'\
            u'Глава 1\n'\
            u'Общие положения\n'\
                u'\n'\
                u'Статья 2. Налоговое законодательство Кыргызской Республики\n'\
                    u'\n'\
                    u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                    u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                    u'3. Настоящий Кодекс устанавливает:...\n'\
                    u'\n'
            u'РАЗДЕЛ XIV. Я РАЗДЕЛ XIV'
                u'\n'
                u'Статья 3. Цели регистрации\n'
                    u'\n'\
                    u'Регистрация осуществляется в целях:\n'\
                    u'- удостоверения факта создания, внесения изменений и дополнений в государственный реестр, а также...\n'\
                    u'- учета зарегистрированных (перерегистрированных) и прекративших деятельность юридических лиц, филиалов (представительств);\n'\
                    u'- ведения государственного реестра;\n'\
                    u'- предоставления заинтересованным физическим и юридическим лицам информации о зарегистрированных (перерегистрированных)...'
        )

        expected_sections = []

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        expected_sections.append(article)

        chapter = Section('chapter', name=u'Глава 1 Общие положения', number='1')

        article = TextSection(level='article', name=u'Статья 2. Налоговое законодательство Кыргызской Республики', number='2')

        item = TextSection(level='article2_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        chapter.add_section(article)

        expected_sections.append(chapter)

        division = Section('division', name=u'РАЗДЕЛ XIV. Я РАЗДЕЛ XIV', number='XIV')

        article = TextSection('article', name=u'Статья 3. Цели регистрации', number='3')
        article.text = \
            u'Регистрация осуществляется в целях:\n'\
            u'- удостоверения факта создания, внесения изменений и дополнений в государственный реестр, а также...\n'\
            u'- учета зарегистрированных (перерегистрированных) и прекративших деятельность юридических лиц, филиалов (представительств);\n'\
            u'- ведения государственного реестра;\n'\
            u'- предоставления заинтересованным физическим и юридическим лицам информации о зарегистрированных (перерегистрированных)...'

        division.add_section(article)

        expected_sections.append(division)

        actual_sections = builder.build_sections()
        self.assertEqual(expected_sections, actual_sections)

    def test_build_part_with_articles(self):
        builder = Builder(
            u'ОБЩАЯ ЧАСТЬ\n'\
                '\n'\
                u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской\n'\
                u'Республики\n'\
                    u'\n'\
                    u'1. Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...\n'\
                    u'2. Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.\n'\
                    u'3. К отношениям по взиманию налогов с перемещаемых через таможенную границу...\n'\
                    u'\n'\
                u'Статья 2. Налоговое законодательство Кыргызской Республики\n'\
                    u'\n'\
                    u'1. Налоговое законодательство Кыргызской Республики - это система нормативных правовых...\n'\
                    u'2. Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...\n'\
                    u'3. Настоящий Кодекс устанавливает:...\n'\
                    u'\n'
                u'Статья 3. Действие международных договоров и иных соглашений\n'\
                    u'\n'\
                    u'1. Если вступившим в установленном законом порядке международным договором, участником...\n'\
                    u'2. Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
                    u'\n'\
        )

        expected_parts = []

        part = Section('part', name= u'ОБЩАЯ ЧАСТЬ', number='1')

        article = TextSection(level='article', name=u'Статья 1. Отношения, регулируемые Налоговым кодексом Кыргызской Республики', number='1')

        item = TextSection(level='article1_item', name='', number='1')
        item.text = u'Налоговый кодекс Кыргызской Республики (далее - Кодекс) регулирует отношения...'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='2')
        item.text = u'Отношения, регулируемые настоящим Кодексом, являются налоговыми правоотношениями.'
        article.add_section(item)

        item = TextSection(level='article1_item', name='', number='3')
        item.text = u'К отношениям по взиманию налогов с перемещаемых через таможенную границу...'
        article.add_section(item)

        part.add_section(article)

        article = TextSection(level='article', name=u'Статья 2. Налоговое законодательство Кыргызской Республики', number='2')

        item = TextSection(level='article2_item', name='', number='1')
        item.text = u'Налоговое законодательство Кыргызской Республики - это система нормативных правовых...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='2')
        item.text = u'Налоговое законодательство Кыргызской Республики состоит из следующих нормативных правовых актов:...'
        article.add_section(item)

        item = TextSection(level='article2_item', name='', number='3')
        item.text = u'Настоящий Кодекс устанавливает:...'
        article.add_section(item)

        part.add_section(article)

        article = TextSection(level='article', name=u'Статья 3. Действие международных договоров и иных соглашений', number='3')

        item = TextSection(level='article3_item', name='', number='1')
        item.text = u'Если вступившим в установленном законом порядке международным договором, участником...'
        article.add_section(item)

        item = TextSection(level='article3_item', name='', number='2')
        item.text = u'Если соглашение, заключенное Правительством Кыргызской Республики, ратифицировано...'
        article.add_section(item)

        part.add_section(article)

        expected_parts.append(part)

        actual_parts = builder.build_sections()
        self.assertEqual(expected_parts, actual_parts)