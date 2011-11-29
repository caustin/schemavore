from collections import namedtuple
from descriptors import XmlInstanceElement, ImmutableAttributeDescriptor, NonNegativeAttributeDescriptor, ComplexXmlSchemaNode
from descriptors import BaseValueDescriptor, StringValueDescriptor
from descriptors import SimpleXmlSchemaNode, XmlNode
from namespace import  Xsd


TypeInformation = namedtuple("TypeInformation", "type_name namespace")

class ModelBase(object):
    """
    """

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

    type_name = ImmutableAttributeDescriptor("type_name", "xsd_type_info")
    namespace = ImmutableAttributeDescriptor("namespace", "xsd_type_info")
    schema_node = SimpleXmlSchemaNode()
    value = BaseValueDescriptor()
    xml_node = XmlNode()


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

    def __init__(self, name, **kwargs):
        """
        @param: name
        @param: default
        @param: fixed
        @param: attributes
        @param: min_occurs
        @param: max_occurs
        @param: nillable

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
            attributes:
                xml attributes.
                    either a list of tuples....
                    or a dictionary object....
                    but how can attributes be assigned on the fly?
                    etree supports a element.set('attribute', 'value') and assigning attributes a creation.
                    --> just expose the dict for now.
        """

        self.name = name
        self.default = kwargs.get("default")
        self.fixed = kwargs.get("fixed")
        self._val = None

        # Per http://www.w3.org/TR/xmlschema-0/ the defaul value for min and max
        # occurs is 1
        self.min_occurs = kwargs.get("min_occurs", 1)
        self.max_occurs = kwargs.get("max_occurs", 1)
        self.attributes = kwargs.get('attributes', {})

        # The default value for nillable is False
        self.nillable = kwargs.get('nillable', False)
        
        # validate indicators
        self.__validate_occurrence_indicators()

        # validate nillable
        self.__validate_nillable()

    def __validate_occurrence_indicators(self):

        if not str(self.max_occurs).isdigit() and self.max_occurs != "unbounded":
            raise ValueError(
                "max_occurs must be a positve integer or unbounded"
            )

        elif not str(self.min_occurs).isdigit():
            raise ValueError(
                "min_occurs must be a positive integer"
            )

        elif self.min_occurs > self.max_occurs:
            raise ValueError("min_occurs must be less than max_occurs")

        elif self.min_occurs < 0 or self.max_occurs < 0 :
            raise ValueError(
                "min_occurs and max_occurs must be greater than zero"
            )
        else:
            return

    def __validate_nillable(self):
        if self.nillable not in [True, False] :
            raise ValueError("nillable must be either True or False")
        else :
            return

        





class Attribute(ModelBase):
    """Attributes type modeled after XML Attributes.

    Attrubutes *must* be passed a TypeInformation named tuple in order to
    resolve the Attribute's type.



    The XML syntax for defining an attribute is as follows:

        <xs:attribute name="xxx" type="yyy"/>

        attributes support:
            Default
            Fixed

        use:
            Attributes are optional by default, to specify that it is required
            us the "use" attribute
            <xs:attribute name="lang" type="xs:string" use="required"/>

        type_information:
            The type of the attribute....perhaps these should be subclasses of
            ModelBase???????
            Work with that for now....see how well it works in real situations
            to determine if it needs to be tweaked.


        Currently, only strings are supported...as the project matures,
        attributes will need to be flexible.  This can be done via inheritance
        or some other more interesting means.
    """

    namespace = None
    type_name = None
    schema_node = SimpleXmlSchemaNode(element_name="attribute")

    # TODO: Attributes only support string types..since that is all this
    # project supports at the present.  Fix this
    def __init__(self, name, **kwargs):
        """
        @param name:
        @param default:
        @oaram fixed
        @param use: Boolean.  Indicates that the attribute is required.  Default is false.
        @param type_information: TypeInformation tuple.
        """
        self.creation_counter = ModelBase.creation_counter
        ModelBase.creation_counter += 1

        self.use = kwargs.get("use", False)
        self.type_information = kwargs.get("type_information", String.xsd_type_info)

        self.type_name = self.type_information.type_name
        self.namespace = self.type_information.namespace
        self.restrictions = False

        super(Attribute, self).__init__(name, **kwargs)

    

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

    value = StringValueDescriptor()

    def __init__(self, name, **kwargs):
        """
        @param: name: The name of the instance element...not the type name.
        @param: default: The default value for the element's value.  This is
                    used whenever the value is not set explicitly
        @param: fixed: A fixed value for the element's value.  This cannot be
                    used in conjunction with default and will result in the
                    value not being set if it is explicitly passed.
        @param: attributes
        @param: enumeration: Defines a list of acceptable values
        @param: length: Specifies the exact number of characters or list items
                    allowed. Must be equal to or greater than zero
        @param: min_length: Specifies the minimum number of characters
                    allowed. Must be equal to or greater than zero.
        @param: max_length: Specifies the maximum number of characters
                    allowed. Must be equal to or greater than zero and greater
                    than min_length if specified.
        @param: pattern: Defines the exact sequence of characters that are
                    acceptable.  NOT CURRENTLY IMPLEMENTED
        @param: white_space: Specifies how white space is handled.
        @param: min_occurs: The minimum number of occurrences of this element in
                    an xml instance.  Must be greater than or equal to zero
                    and less than max_occurs if it is specified.
        @param: max_occurs: The maximum number of occurrences of this element in
                    an xml instance.  Must be greater than or equal to zero
                    and greater than min_occurs if it is specified.
        @param: nillable: Specifies whether or not an element is required in
                    an instance document.  If true then then element is not
                    required in the instance document.  If false then the
                    element is required.  Default is false.

        Restrictions:
            enumeration:
            length:
            max_length:
            minLength:
            pattern
            whiteSpace:

        """

        self.restrictions = False
        self.max_length = kwargs.get("max_length")
        self.min_length = kwargs.get("min_length")
        self.length = kwargs.get("length")
        self.enumeration = kwargs.get("enumeration")


        if self.length or self.max_length or self.min_length or self.enumeration:
            self.restrictions = True

        self.creation_counter = ModelBase.creation_counter
        ModelBase.creation_counter += 1
        
        super(String, self).__init__(name,  **kwargs)

    def __repr__(self):
        return "String(%s, %s)" % (self.name, self.value)

    def __str__(self):
        if self.value:
            return self.value
        else:
            return self.name


class ComplexModel(ModelBase):
    """
    Represents a complex element.  The default XSD representation that should
    be used for complex elements is...

    <xs:element name="employee" type="personinfo"/>

    <xs:complexType name="personinfo">
        <xs:sequence>
            <xs:element name="firstname" type="xs:string"/>
            <xs:element name="lastname" type="xs:string"/>
        </xs:sequence>
    </xs:complexType>

    see (http://www.w3schools.com/schema/schema_complex_elements.asp)

    To support empty complex types, it is necessary to render the xsd properly...see (http://www.w3schools.com/schema/schema_complex_empty.asp)
    """

    #TODO: Add support for order indicators....
    # Possible choices are "All", "Sequence", "Choice"

    #TODO: Add support for Group Indicators.
    # Possible choices are "Group Name", "attributeGroupName"

    schema_node = ComplexXmlSchemaNode()

    def __init__(self, name, **kwargs):
        super(ComplexModel, self).__init__(name, **kwargs)

        #TODO: Implement This on the descriptor side !!!!
        self.order_indicator = kwargs.get("order_indicator", "sequence")

        self.creation_counter = ModelBase.creation_counter
        ModelBase.creation_counter += 1


    @classmethod
    def get_child_nodes(cls):

        nodes = dict()

        for key, value in cls.__dict__.iteritems():
            if issubclass(value.__class__, ModelBase):
                nodes[key] = value

        for key, value in sorted(
                nodes.items(), key=lambda (key, value):
                (value.creation_counter, key)):

                 yield value

