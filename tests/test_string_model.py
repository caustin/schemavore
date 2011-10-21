
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
        self.text = "text"
        self.tag = "tag"
        self.name = "name"
        self.string_model = String(self.tag, self.text, name=self.name)

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
        self.assertEquals(self.text, self.string_model.text)

    def test_tag(self):
        self.assertEquals(self.tag, self.string_model.tag)

    def test_name(self):
        self.assertEquals(self.name, self.string_model.name)

    def test_default(self):
        s = String(self.tag, None, name=self.name, default="default")
        self.assertEquals("default", s.text)

    def test_default_with_text(self):
        s = String(self.tag, self.text, name=self.name, default="default")
        self.assertEquals(self.text, s.text)

    def test_fixed(self):
        s = String(self.tag, None, name=self.name, fixed="fixed")
        self.assertEquals("fixed", s.text)

    def test_fixed_with_text(self):
        s = String(self.tag, self.text, name=self.name, fixed="fixed")
        self.assertEquals("fixed", s.text)

    def test_fixed_with_default(self):
        s = String(self.tag, None, name=self.name, fixed="fixed", default="default")
        self.assertEquals("fixed", s.text)

    def test_fixed_with_default_and_text(self):
        s = String(self.tag, self.text, name=self.name, fixed="fixed", default="default")
        self.assertEquals("fixed", s.text)

    def test_from_xml(self):
        self.assertEquals(
            type(String.from_string("<bad>good</bad>")),
            type(String)
        )

    def test_from_element(self):
        self.assertEquals(
            type(String.from_element(etree.fromstringlist("<a>b</a>"))),
            type(String)
        )

    def test_xml(self):
        tag = get_prefix_tag(NS_XSD_PREFIX, self.tag)
        prefix_binding = get_prefix_binding(NS_XSD_PREFIX, NS_XSD)
        expected_xml = "<{0:>s} {1:>s}>{2:>s}</{3:>s}>".format(
            tag, prefix_binding, self.text, tag
        )
        self.assertEquals(expected_xml, self.string_model.xml.strip())

    def test_ns_map(self):
        element = self.string_model.element
        nsmap = {NS_XSD_PREFIX:NS_XSD}
        self.assertEquals(nsmap, element.nsmap)

    def test_xsd(self):

        xsd = self.string_model.xml_schema
        print xsd
        self.assertFalse(True)