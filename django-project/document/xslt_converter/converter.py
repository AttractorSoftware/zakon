# coding=utf-8
import os
from lxml import etree
from zakon.settings import PROJECT_ROOT


class XsltTransformer(object):

    @classmethod
    def transform_to_html(self, content):
        f = open(os.path.join(PROJECT_ROOT, 'document', 'xslt_converter', 'template.xsl'))
        result_xsl = f.read()
        xml_result = etree.XML(content)
        xslt_root = etree.XML(result_xsl)
        transform = etree.XSLT(xslt_root)
        html = transform(xml_result)
        result = etree.tostring(html)
        #will return string which between <html>...</html>
        start_content = 6
        end_content = len(result)-7
        return result[start_content:end_content]