#!/usr/bin/python
#coding=utf-8
import sys
import libxml2
import libxslt


def getXSLT(xsl_filename):
    # parse the stylesheet xml file into doc object
    styledoc = libxml2.parseFile(xsl_filename)

    # process the doc object as xslt
    style = libxslt.parseStylesheetDoc(styledoc)

    return style


if __name__ == '__main__':
    style = getXSLT("template.xsl")
    doc = libxml2.parseFile("example.xml")
    result = style.applyStylesheet(doc, None)
    result = str(result).decode('utf-8')

    f = open('output.html', 'r+')
    f.write(str(result))

    print result