# coding=utf-8
from lxml import etree

class XsltTransformer(object):

    def __init__(self):
        self._xml_result = ''

    def transform(self, content):
        f = open('template.xsl')
        result_xsl = f.read()
        self._xml_result = etree.XML(content)
        xslt_root = etree.XML(result_xsl)
        transform = etree.XSLT(xslt_root)
        html = transform(self._xml_result)
        return etree.tostring(html)






