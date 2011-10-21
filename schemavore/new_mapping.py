__author__ = 'chris'

import lxml.objectify
import lxml.etree


class Attributes(object):

    def __get__(self, instance, owner):

        if type(instance._attributes) is not type(list):
            raise AttributeError("Must be a list")
        else:
            return instance._attributes

    def __set__(self, instance, value):
        raise AttributeError("Cannot be set")

    def __delete__(self, instance):
        raise AttributeError("Cannot be deleted")



class String(object):

    def __init__(self, tag, text, attributes=None):
        self.tag = tag
        self.text = text
        self._attributes = attributes


    def xml(self):
        element = lxml.etree.Element(self.tag)
        element.text = self.text
        print lxml.etree.tostring(element)

        element.text = self.text

        print element
        print lxml.etree.tostring(element, pretty_print=True)

        return lxml.etree.tostring(element, pretty_print=True)
    
    attributes = Attributes()
