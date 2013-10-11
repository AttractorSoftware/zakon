#from lxml import etree
#
#
#class AddReference(object):
#    def add_node_reference(self, document_content, object_id, start_position, end_position, link_document_id,
#                           link_object_id):
#
#        xml_parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
#
#        mxml = etree.fromstring(document_content, parser=xml_parser)
#
#        expr = ".//*[@id='" + object_id + "']"
#
#        child_index = 0
#        for node in mxml.xpath(expr):
#            if node.attrib['id'] == object_id:
#
#                text = node.text if node.text else ''
#                if start_position < len(text) >= end_position:
#                    self._add_node(node, text, start_position, end_position, child_index, link_document_id,
#                                   link_object_id)
#                else:
#                    for child in node.getchildren():
#                        text += child.text
#                        child_index += 1
#                        tail_text = child.tail if child.tail else ''
#
#                        if len(text) <= start_position < len(text + tail_text) and end_position <= len(
#                                        text + tail_text):
#                            self._add_node_tail(node, child, child_index, text, tail_text, start_position, end_position,
#                                                link_document_id, link_object_id)
#
#                        text += tail_text
#
#        return etree.tostring(mxml, encoding='utf-8')
#
#    def _add_node(self, node, text, start_position, end_position, child_index, link_document_id, link_object_id):
#
#        element = etree.Element('reference', document_id=link_document_id, object_id=link_object_id)
#        element.text = text[start_position:end_position]
#        node.insert(child_index, element)
#        node.text = text[:start_position]
#        element.tail = text[end_position:]
#
#    def _add_node_tail(self, node, child, child_index, text, tail_text, start_position, end_position, link_document_id,
#                       link_object_id):
#
#        text_length = len(text)
#        common_text = text + tail_text
#        child.tail = common_text[text_length:start_position]
#
#        element = etree.Element('reference', document_id=link_document_id, object_id=link_object_id)
#        element.text = common_text[start_position:end_position]
#        element.tail = common_text[end_position:]
#        node.insert(child_index, element)
#
#
