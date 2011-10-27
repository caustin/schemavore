from collections import namedtuple
from descriptors import XmlInstanceElement, ImmutableAttributeDescriptor
from descriptors import XmlSchemaNode, XmlNode
from namespace import  Xsd


TypeInformation = namedtuple("TypeInformation", "type_name namespace")

class ModelBase(object):
    """
    """

    # ---------- Class Attributes ---------- #
    # Used to track the order that objects are created. Used to ensure the
    # rendering order for elements in a sequence matches the order they are
    # declared in the model
    creation_counter = 0

    # Fixed Class Attributes....There might be a way to build better immutable
    # attributes but I can't think of any besides doing something with a
    # property or descriptor and this seems simpler.  However, this may be a
    # violation of the DRY principle for whatever it is worth in this context.
    xsd_type_info = TypeInformation(type_name=None, namespace=None)
    element = XmlInstanceElement()

    # ---------- Descriptors ---------- #
    type_name = ImmutableAttributeDescriptor("type_name", "xsd_type_info")
    namespace = ImmutableAttributeDescriptor("namespace", "xsd_type_info")
    schema_node = XmlSchemaNode()
    xml = XmlNode()

    # ---------- Class Methods ---------- #
    @classmethod
    def from_string(cls, string):
        raise NotImplementedError

    @classmethod
    def from_element(cls, element):
        raise NotImplementedError

    # ---------- Overrides ---------- #
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

    def __init__(self, name, value, **kwargs):
        """
        Possible kwargs are:
            name :
                The name of the instance element, not to be confused with the
                type name
            default:
                The default value for the element's value.  This is used
                whenever the value is not set explicitly
            fixed:
                A fixed value for the element's value.  This cannot be used in
                conjunction with default and will result in the value not being
                set if it is explicitly passed.
        """

        self.name = name
        self.default = kwargs.get("default")
        self.fixed = kwargs.get("fixed")


        if self.fixed is not None :
            self.value = self.fixed
        elif value is None:
            if self.default is not None:
                self.value = self.default
            else:
                self.value = value
        else :
            self.value = value

    def validate(self, *args, **kwargs):
        """Method to
        """

        # TODO: Figure out a more better :) way to handle this.
        return self.name is not None and type(self.name) is type(str)


class String(ModelBase):
    """
    """

    xsd_type_info = TypeInformation(type_name="string", namespace=Xsd.namespace)
    prefix = Xsd.prefix

    #todo: Implement a validate() type method in the base class and have it
    # implemented by the subclasses

    #todo: Model Behaviour Test
    #todo: ModelTest for pattern        -- defered to later
    #todo: ModelTest for whiteSpace     -- defered to later

    #todo: XSDNode Rendering and Validation Tests
    #todo: XSDNodeTest for pattern
    #todo: XSDNodeTest for whiteSpace

    #todo: XML Rendering test
    #todo: XMLTest for enumeration
    #todo: XMLTest for length
    #todo: XMLTest for maxLength
    #todo: XMLTest for minLength
    #todo: XMLTest for pattern
    #todo: XMLTest for whiteSpace

    def __init__(self, name, value, **kwargs):
        """
        @param: name: The name of the instance element...not the type name.
        @param: value: The value of the instance element

        Possible kwargs are:
            name :   The name of the instance element, not to be confused with
                     the type name

            default:
                The default value for the element's value.  This is used
                whenever the value is not set explicitly

            fixed:
                A fixed value for the element's value.  This cannot be used in
                conjunction with default and will result in the value not being
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
                    NOT CURRENTLY IMPLEMENTED
                    Defines the exact sequence of characters that are acceptable
                whiteSpace:
                    NOT CURRENTLY IMPLEMENTED
                    Specifies how white space (line feeds, tabs, spaces, and
                    carriage returns) is handled
        """

        self.max_length = kwargs.get("max_length")
        self.min_length = kwargs.get("min_length")
        self.length = kwargs.get("length")
        self.enumeration = kwargs.get("enumeration")


        if self.length :
            if len(value) != self.length:
                raise AttributeError("Length of value is not the same a the specified length")
    
        elif self.max_length and len(value) > self.max_length:
            raise AttributeError("Length of value is greater than the specified max_length")
        elif self.max_length and self.min_length:
            if self.max_length < self.min_length:
                raise AttributeError("The specified max_length is less than the specified min_length")
        elif self.min_length and len(value) < self.min_length:
            raise AttributeError("Length of value is less than the specified min_length")

        elif self.enumeration:
            if value not in self.enumeration:
                raise AttributeError("value not in specified enumeration")


        
        super(String, self).__init__(name, value, **kwargs)

    def __repr__(self):
        return "String(%s, %s)" % (self.name, self.value)

    def __str__(self):
        return self.value

    