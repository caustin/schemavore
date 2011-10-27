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


class XmlSchemaNode(object):
    """Represents the schema node of an individual XSD element. 
    """

    def __init__(self):
        self.restriction = None


    def _build_restrictions(self, instance):
        simple_tag = "{%s}simpleType" % instance.namespace
        simple = etree.SubElement(self.element, simple_tag)
        rest_tag = "{%s}restriction" % instance.namespace
        base = "%s:%s" % (instance.prefix, instance.type_name)
        self.restriction = etree.SubElement(simple, rest_tag)
        self.restriction.set("base", base)




    def _build_enumeration(self, instance):
        if self.restriction is None:
            self._build_restrictions(instance)

        for enum in instance.enumeration:
            etree.SubElement(self.restriction, "{%s}enumeration" % instance.namespace).set("value", enum)

    def __get__(self, instance, owner=None):

        if instance.type_name is None:
            raise ValueError("type_name Must Not be None!")
        elif instance.namespace is None:
            raise ValueError("namespace must not be None.")

        tag = "{%s}%s" % (instance.namespace, "element")
        self.element = etree.Element(tag, nsmap=primitive_nsmap)
        self.element.set("name", instance.name)
        self.element.set("type", "%s:%s" % (Xsd.prefix, instance.type_name))

        if instance.default:
            self.element.set('default', instance.default)
        elif instance.fixed:
            self.element.set("fixed", instance.fixed)

        if instance.enumeration:
            self._build_enumeration(instance)

        if instance.default:
            self._build_default(instance)

        if instance.fixed:
            self._build_fixed(instance)

        if instance.max_length or instance.min_length:
            self._build_min_max_lenth(instance)

        if instance.length:
            self._build_length(instance)

        return self.element


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