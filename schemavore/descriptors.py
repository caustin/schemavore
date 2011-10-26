from namespace import Xsd, primitive_nsmap
from exceptions import ValueError
import lxml
from lxml import etree


class XmlInstanceElement(object):
    """
    """

    def __get__(self, instance, owner=None):

        if instance is None:
            raise ValueError(
                "This method requires an instance of the Model Class"
                )

        tag = "{%s}%s" % (Xsd.namespace, instance.tag)
        element = etree.Element(tag, nsmap=primitive_nsmap)
        element.text = instance.text

        return element


class Xml(object):
    """
    """

    def __get__(self, instance, owner):

        if instance is None:
            raise ValueError(
                "This Method requires an instance of the Model Class"
            )

        return etree.tostring(instance.element, pretty_print=True)


class XmlSchema(object):
    """
    """

    def __get__(self, instance, owner=None):

        if instance.type_name is None:
            raise ValueError("type_name Must Not be None!")
        elif instance.namespace is None:
            raise ValueError("namespace must not be None.")

        root = etree.Element("root", nsmap=primitive_nsmap)
        tag = "{%s}%s" % (instance.namespace, "element")
        element = etree.Element(tag, nsmap=primitive_nsmap)
        print instance.name
        element.set("name", instance.name)
        element.set("type", "{%s}%s" % (Xsd.namespace , instance.type_name))

        if instance.default:
            element.set('default', instance.default)
        elif instance.fixed:
            element.set("fixed", instance.fixed)

        root.append(element)

        return root


class ImmutableAttributeDescriptor(object):
    """Wraps any container that supports attribute access and enforces
    immutability on the desired attribute.

    This has been tested only with named tuples at this point
    """

    def __init__(self, attribute, attribute_container):
        """
        """
        self._attribute = attribute
        self._attribute_container = attribute_container


    def __check_container(self, instance):
        container = getattr(instance, self._attribute_container)
        if container is None :
            raise AttributeError(
                "target instance is missing 'container' attribute"
            )
        else :
            return container


    def __get__(self, instance, owner=None):
        container = self.__check_container(instance)
        attr_value = getattr(container, self._attribute)
        return attr_value


    def __set__(self, instance, value):
        self.__check_container(instance)
        raise AttributeError("can't set attribute")


    def __delete__(self, instance):
        self.__check_container(instance)
        raise AttributeError("can't delete attribute")