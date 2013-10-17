# -*- coding: utf-8 -*-
from lxml import etree
from document.models import Document
from References.models import Reference
from document.views import render
from References.forms import WrapTextForm
from StringIO import StringIO


def add_sub_refs(linked_doc_id, linked_element, references_tag):
    reference_tag = etree.SubElement(references_tag, "reference")
    reference_tag.set("linked_doc_id", "" + linked_doc_id.__str__() + "")
    reference_tag.set("linked_element", "" + linked_element.__str__() + "")


def add_sub_links(reference_doc_id, reference_element, links_tag):
    link_tag = etree.SubElement(links_tag, "link")
    link_tag.set("reference_doc_id", "" + reference_doc_id.__str__() + "")
    link_tag.set("reference_element", "" + reference_element.__str__() + "")


def remove_sharp(element):
    return element.replace("#", "")


def update_xml_of_reference_document(reference_content, reference_element, linked_doc_id, linked_element):
    """
     Контент документа,
     Элемент документа с которого ссылаемся,
     ID документа на кототорый ссылаемся,
     Элемент на который ссылаемся
     """

    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    tree = etree.parse(StringIO(reference_content), parser)
    root = tree.getroot()
    selected_reference_element = root.xpath("//article[@id='" + remove_sharp(reference_element) + "']")[0]

    if selected_reference_element.find("references") is None:
        references_tag = etree.SubElement(selected_reference_element, "references")
        add_sub_refs(linked_doc_id, remove_sharp(linked_element), references_tag)
    else:
        references_tag = selected_reference_element.xpath("//references")[0]
        add_sub_refs(linked_doc_id, remove_sharp(linked_element), references_tag)
    return etree.tostring(root, pretty_print=True)


def update_xml_of_linked_document(linked_content, linked_element, reference_doc_id, reference_element):
    """
     Контент документа,
     Элемент документа на который ссылаемся,
     ID документа с кототорого ссылаемся,
     Элемент с которого ссылаемся
     """

    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    tree = etree.parse(StringIO(linked_content), parser)
    root = tree.getroot()
    selected_reference_element = root.xpath("//article[@id='" + remove_sharp(linked_element) + "']")[0]

    if selected_reference_element.find("links") is None:
        links_tag = etree.SubElement(selected_reference_element, "links")
        add_sub_links(reference_doc_id, remove_sharp(reference_element), links_tag)
    else:
        links_tag = selected_reference_element.xpath("//links")[0]
        add_sub_links(reference_doc_id, remove_sharp(reference_element), links_tag)
    return etree.tostring(root, pretty_print=True)


def wrap_text_in_tag(request):
    if request.method == 'POST':
        form = WrapTextForm(request.POST)
        if form.is_valid():

            ref = Reference()
            ref.reference_document = Document.objects.get(pk=request.POST.get('reference_document_id'))
            ref.reference_element = request.POST.get('reference_element')
            ref.linked_document = Document.objects.get(pk=request.POST.get('linked_document_id'))
            ref.linked_element = request.POST.get('linked_element')

            reference_document = ref.reference_document
            linked_document = ref.linked_document

            ref.save()
            """Вызывать ID тебе нужно, юный падаван, вовсе не документа объект, бдителен будь!"""
            reference_document.content = update_xml_of_reference_document(reference_document.content,
                                                                          ref.reference_element, ref.linked_document.id,
                                                                          ref.linked_element)
            linked_document.content = update_xml_of_linked_document(linked_document.content, ref.linked_element,
                                                                    ref.reference_document.id,
ref.reference_element)
            reference_document.save()
            linked_document.save()

    return render(request, 'document/list.html', {'documents': Document.objects.all()})
