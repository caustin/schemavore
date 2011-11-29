from exceptions import ValueError
import lxml.etree as etree
from namespace import Xsd, primitive_nsmap

__author__ = 'chris'
class XmlInstanceElement(object):
    """
    """

    def __get__(self, instance, owner=None):

        if instance is None:
            raise ValueError(
                "This method requires an instance of the Model Class"
                )

        tag = "{%s}%s" % (Xsd.namespace, instance.name)
        element = etree.Element(tag, nsmap=primitive_nsmap)
        element.text = instance.value

        return element


class XmlNode(object):
    """Represents the XML instance element
    """

    def __get__(self, instance, owner):

        if instance is None:
            raise ValueError(
                "This Method requires an instance of the Model Class"
            )

        return etree.tostring(instance.element, pretty_print=True)