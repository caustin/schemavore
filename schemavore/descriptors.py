from namespace import Xsd, primitive_nsmap
from exceptions import ValueError
import lxml
from lxml import etree


#TODO: See if this exists in the std lib.
#TODO: Consider doing this as a decorator.
class NonNegativeAttributeDescriptor(object):
    """
    """

    def __init__(self, attribute_name):
        """
        @param attribute_name: The numeric attribute that should be treated as
        a Non-Negative/positve attribute
        """
        self.attribute = attribute_name

    def __get__(self, instance, owner=None):
        return getattr(instance, self.attribute)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("%s must be a positive value" % self.attribute)
        else:
            setattr(instance, self.attribute, value)

            

class BaseValueDescriptor(object):
    """
    """

    def __get__(self, instance, owner=None):

        if instance.fixed :
            return instance.fixed

        elif instance.default and instance._val is None :
            return instance.default

        else :
            return instance._val

    
    def __set__(self, instance, value):
        instance._val = value

    def __delete__(self, instance):
        instance._val = None

class StringValueDescriptor(BaseValueDescriptor):
    """
    """

    def __set__(self, instance, value):

        if instance.length :
            if len(value) != instance.length:
                raise AttributeError(
                    "Length of value is not the same a the specified length"
                )

        elif instance.max_length or instance.min_length:
            if instance.max_length and len(value) > instance.max_length:
                raise AttributeError(
                    "Length of value is greater than the specified max_length"
                )

            elif instance.max_length and instance.min_length:
                if instance.max_length < instance.min_length:
                    raise AttributeError(
                        "The max_length is less than the min_length"
                    )

            if instance.min_length and len(value) < instance.min_length:
                raise AttributeError(
                    "Length of value is less than the specified min_length"
                )

        elif instance.enumeration:
            if value not in instance.enumeration:
                raise AttributeError("value not in specified enumeration")

        super(StringValueDescriptor, self).__set__(instance, value)





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

    def __init__(self, element_name="element"):
        self.element_name = element_name


    def _build_restrictions(self, instance):
        simple_tag = "{%s}simpleType" % instance.namespace
        simple = etree.SubElement(self.element, simple_tag)
        rest_tag = "{%s}restriction" % instance.namespace
        base = "%s:%s" % (instance.prefix, instance.type_name)
        restriction = etree.SubElement(simple, rest_tag)
        restriction.set("base", base)

        return restriction

    def _build_occurs(self, instance):
        pass

    def _build_enumeration(self, instance, restriction):
        for enum in instance.enumeration:
            etree.SubElement(
                restriction, "{%s}enumeration" % instance.namespace
            ).set("value", enum)

    def _build_length(self, instance, restriction):
        etree.SubElement(
            restriction, "{%s}length" % instance.namespace
        ).set("value", str(instance.length))


    def _build_min_max_lenth(self, instance, restriction):

        if instance.min_length:
            etree.SubElement(
                restriction, "{%s}minLength" % instance.namespace
            ).set("value", str(instance.min_length))

        if instance.max_length:
            etree.SubElement(
                restriction, "{%s}maxLength" % instance.namespace
            ).set("value", str(instance.max_length))


    def __get__(self, instance, owner=None):

        if instance.type_name is None:
            raise ValueError("type_name Must Not be None!")
        elif instance.namespace is None:
            raise ValueError("namespace must not be None.")

        tag = "{%s}%s" % (instance.namespace, self.element_name)
        self.element = etree.Element(tag, nsmap=primitive_nsmap)
        self.element.set("name", instance.name)

        if not instance.restrictions:
            self.element.set("type", "%s:%s" % (Xsd.prefix, instance.type_name))

        if instance.default:
            self.element.set('default', instance.default)
        elif instance.fixed:
            self.element.set("fixed", instance.fixed)

        # minOccurs XSD default is 1
        if instance.min_occurs != 1:
            self.element.set("minOccurs", str(instance.min_occurs))

        # maxOccurs XSD default is 1
        if instance.max_occurs != 1:
            self.element.set("maxOccurs", str(instance.max_occurs))

        if instance.restrictions:
            restriction = self._build_restrictions(instance)

            if instance.enumeration:
                self._build_enumeration(instance, restriction)

            if instance.max_length or instance.min_length:
                self._build_min_max_lenth(instance, restriction)

            if instance.length:
                self._build_length(instance, restriction)

        # handle required attributes
        if getattr(instance, "use", False):
            self.element.set("use", "required")

        return self.element

#TODO: Add nillable support


class ImmutableAttributeDescriptor(object):
    """Wraps any container that supports attribute access and enforces
    immutability on the desired attribute.

    This has been tested only with named tuples at this point
    """

    def __init__(self, attribute_name, attribute_container):
        """
        """
        self._attribute = attribute_name
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