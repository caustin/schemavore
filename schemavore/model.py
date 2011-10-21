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


class String(ModelBase):
    """
    """

    xsd_type_info = TypeInformation(type_name="string", namespace=Xsd.namespace)

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

            enumeration:
            length:
            maxLength:
            minLength:
            pattern (NMTOKENS, IDREFS, and ENTITIES cannot use this constraint):
            whiteSpace:
        """
        super(String, self).__init__(tag, text, **kwargs)