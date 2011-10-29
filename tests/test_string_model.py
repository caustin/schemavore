
import unittest

from lxml import etree
from schemavore.model import String

NS_XSD = "http://www.w3.org/2001/XMLSchema"
NS_XSD_PREFIX = "xs"

def get_prefix_tag(namespace_prefix, tag):
    return "{0:>s}:{1:>s}".format(namespace_prefix, tag)

def get_prefix_binding(namespace_prefix, namespace):
    return 'xmlns:{0:>s}="{1:>s}"'.format(namespace_prefix, namespace)

class TestSimpleString(unittest.TestCase):

    def setUp(self):
        self.value = "text"
        self.name = "name"
        self.name = "name"
        self.string_model = String(self.name)
        self.string_model.value = self.value

    # removing because name is redundant with name....will reconsider renaming.....name to name and text to value!!!!!
    def set_type_name(self):
        self.string_model.type_name = "foo"

    def set_namespace(self):
        self.string_model.namespace = "bar"

    def set_xsd_type_info(self):
        self.string_model.xsd_type_info = None

    def test_type_name(self):
        self.assertEquals(self.string_model.type_name, "string")

    def test_namespace(self):
        self.assertEquals(self.string_model.namespace, NS_XSD)

    def test_immutable_type_name(self):
        self.assertRaises(AttributeError, self.set_type_name)

    def test_immutable_namespace(self):
        self.assertRaises(AttributeError, self.set_namespace)

    def test_immutable_xsd_type_info(self):
        self.assertRaises(AttributeError, self.set_xsd_type_info)

    def test_text(self):
        self.assertEquals(self.value, self.string_model.value)

    def test_tag(self):
        self.assertEquals(self.name, self.string_model.name)

    def test_name(self):
        self.assertEquals(self.name, self.string_model.name)

    def test_default(self):
        s = String(self.name, default="default")
        self.assertEquals("default", s.value)

    def test_default_with_text(self):
        s = String(self.name, default="default")
        s.value = self.value
        self.assertEquals(self.value, s.value)

    def test_fixed(self):
        s = String(self.name, fixed="fixed")
        s.value = "A"
        self.assertEquals("fixed", s.value)

    def test_fixed_with_text(self):
        s = String(self.name, fixed="fixed")
        s.value = self.value
        self.assertEquals("fixed", s.value)

    def test_fixed_with_default(self):
        s = String(self.name, fixed="fixed", default="default")
        self.assertEquals("fixed", s.value)

    def test_fixed_with_default_and_text(self):
        s = String(self.name, fixed="fixed", default="default")
        s.value = self.value
        self.assertEquals("fixed", s.value)

    def test_from_xml(self):
        self.assertEquals(
            type(String.from_string("<bad>good</bad>")),
            type(String)
        )

    def test_enumeration_value(self):
        enum_vals = ["A", "B", "C", "D"]
        s = String(self.name, enumeration=enum_vals)
        self.assertEquals(enum_vals, s.enumeration)


    def test_enumeration_violation(self):
        enum_vals = ["A", "B", "C", "D"]
        self.assertRaises(AttributeError, self._build_string, self.name, self.value, enumeration=enum_vals)



    def test_max_length_value(self):
        ml = 4
        s = String(self.name,  max_length=ml)
        s.value = "ABC"
        self.assertEquals(ml, s.max_length)

    def _build_string(self, tag, text=None, max_length=None, min_length=None, length=None, enumeration=None):
        s =  String(tag,max_length=max_length,min_length=min_length,length=length,enumeration=enumeration)
        s.value = text
        return s

    def test_max_length_violation(self):
        ml = 2
        self.assertRaises(AttributeError, self._build_string, self.name, "ABC", max_length=ml)

    def test_min_length(self):
        min_length = 4
        s = String(self.name, min_length=min_length)
        s.value = "ABCD"
        self.assertEquals(min_length, s.min_length)

    def test_min_length_violation(self):
        min = 4
        self.assertRaises(AttributeError, self._build_string, self.name, "ABC", min_length=min)

    def test_max_less_than_min(self):
        min = 6
        max = 5
        self.assertRaises(AttributeError, self._build_string, self.name, self.value, max_length=max, min_length=min)

    def test_length_value(self):
        s = self._build_string(self.name, text=self.value, length=len(self.value))

        self.assertEquals(len(self.value), s.length)

    def test_length_violation_short(self):
        self.assertRaises(AttributeError, self._build_string, self.name, text=self.value, length=len(self.value)-1)

    def test_length_violation_long(self):
        self.assertRaises(AttributeError, self._build_string, self.name, self.value, length=len(self.value)+1)

    def test_pattern(self):
        raise NotImplementedError

    def test_whitespace(self):
        raise NotImplementedError

    def test_from_element(self):
        self.assertEquals(
            type(String.from_element(etree.fromstringlist("<a>b</a>"))),
            type(String)
        )

#    def test_xml(self):
#        tag = get_prefix_tag(NS_XSD_PREFIX, self.name)
#        prefix_binding = get_prefix_binding(NS_XSD_PREFIX, NS_XSD)
#        expected_xml = "<{0:>s} {1:>s}>{2:>s}</{3:>s}>".format(
#            tag, prefix_binding, self.value, tag
#        )
#        self.assertEquals(expected_xml, self.string_model.xml.strip())

    def test_ns_map(self):
        element = self.string_model.element
        nsmap = {NS_XSD_PREFIX:NS_XSD}
        self.assertEquals(nsmap, element.nsmap)