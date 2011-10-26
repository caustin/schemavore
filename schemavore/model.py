from collections import namedtuple
from descriptors import XmlInstanceElement, ImmutableAttributeDescriptor
from descriptors import XmlSchema, Xml
from namespace import  Xsd


TypeInformation = namedtuple("TypeInformation", "type_name namespace")

class ModelBase(object):
    """
    """

    # Fixed Class Attributes....There might be a way to build better immutable
    # attributes but I can't think of any besides doing something with a
    # property or descriptor and this seems simpler.  However, this may be a
    # violation of the DRY principle for whatever it is worth in this context.
    xsd_type_info = TypeInformation(type_name=None, namespace=None)
    element = XmlInstanceElement()

    # Descriptors
    type_name = ImmutableAttributeDescriptor("type_name", "xsd_type_info")
    namespace = ImmutableAttributeDescriptor("namespace", "xsd_type_info")
    xml_schema = XmlSchema()
    xml = Xml()

    # Class Methods

    @classmethod
    def from_string(cls, string):
        raise NotImplementedError

    @classmethod
    def from_element(cls, element):
        raise NotImplementedError

    def __setattr__(self, key, value):
        if key is "xsd_type_info":
            raise AttributeError("can't set xsd_type_info")
        else:
            super(ModelBase, self).__setattr__(key, value)

    def __delattr__(self, item):
        if item is "xsd_type_info":
            raise AttributeError("can't delete xsd_type_info")
        else:
            super(ModelBase, self).__delattr__(item)

    def __init__(self, tag, text, **kwargs):
        """
        Possible kwargs are:
            name :
                The name of the instance element, not to be confused with the
                type name
            default:
                The default value for the element's text.  This is used
                whenever the text is not set explicitly
            fixed:
                A fixed value for the element's text.  This cannot be used in
                conjunction with default and will result in the text not being
                set if it is explicitly passed.
        """

        self.tag = tag
        self.name = kwargs.get("name")
        self.default = kwargs.get("default")
        self.fixed = kwargs.get("fixed")


        if self.fixed is not None :
            self.text = self.fixed
        elif text is None:
            if self.default is not None:
                self.text = self.default
            else:
                self.text = text
        else :
            self.text = text

    def validate(self, *args, **kwargs):
        """Method to
        """

        # TODO: Figure out a more better :) way to handle this.
        return self.tag is not None and type(self.tag) is type(str)


class String(ModelBase):
    """
    """

    xsd_type_info = TypeInformation(type_name="string", namespace=Xsd.namespace)

    #todo: Implement a validate() type method in the base class and have it
    # implemented by the subclasses

    #todo: Model Behaviour Test
    #todo: ModelTest for pattern -- defered to later
    #todo: ModelTest for whiteSpace -- defered to later

    #todo: XSD Rendering and Validation Tests
    #todo: XSDTest for enumeration
    #todo: XSDTest for length
    #todo: XSDTest for maxLength
    #todo: XSDTest for minLength
    #todo: XSDTest for pattern
    #todo: XSDTest for whiteSpace

    #todo: XML Rendering test
    #todo: XMLTest for enumeration
    #todo: XMLTest for length
    #todo: XMLTest for maxLength
    #todo: XMLTest for minLength
    #todo: XMLTest for pattern
    #todo: XMLTest for whiteSpace

    def __init__(self, tag, text, **kwargs):
        """
        Possible kwargs are:
            name :   The name of the instance element, not to be confused with
                     the type name

            default:
                The default value for the element's text.  This is used
                whenever the text is not set explicitly

            fixed:
                A fixed value for the element's text.  This cannot be used in
                conjunction with default and will result in the text not being
                set if it is explicitly passed.

            Restrictions:
                enumeration:
                    Defines a list of acceptable values
                length:
                    Specifies the exact number of characters or list items
                    allowed. Must be equal to or greater than zero
                maxLength or max_length:
                	Specifies the maximum number of characters or list items
                	allowed. Must be equal to or greater than zero
                minLength:
                    Specifies the minimum number of characters or list items
                    allowed. Must be equal to or greater than zero
                pattern (NMTOKENS, IDREFS, and ENTITIES cannot use this constraint):
                    Defines the exact sequence of characters that are acceptable
                whiteSpace:
                    Specifies how white space (line feeds, tabs, spaces, and
                    carriage returns) is handled
        """

        self.max_length = kwargs.get("max_length")
        self.min_length = kwargs.get("min_length")
        self.length = kwargs.get("length")
        self.enumeration = kwargs.get("enumeration")


        if self.length :
            if len(text) != self.length:
                raise AttributeError("Length of text is not the same a the specified length")
    
        elif self.max_length and len(text) > self.max_length:
            raise AttributeError("Length of text is greater than the specified max_length")
        elif self.max_length and self.min_length:
            if self.max_length < self.min_length:
                raise AttributeError("The specified max_length is less than the specified min_length")
        elif self.min_length and len(text) < self.min_length:
            raise AttributeError("Length of text is less than the specified min_length")

        elif self.enumeration:
            if text not in self.enumeration:
                raise AttributeError("text not in specified enumeration")


        
        super(String, self).__init__(tag, text, **kwargs)

    def __repr__(self):
        return "String(%s, %s)" % (self.tag, self.text)

    def __str__(self):
        return self.text

    