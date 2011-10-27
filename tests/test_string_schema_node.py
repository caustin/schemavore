"""
Test the xsd generation implementation.

The current xsds are implemented as descriptors so in order to test the
implementation it is necassary to first construct an instance of a model
and then grab it's xsd attribute.  This is being tested seperatly because at
the moment is seems like an appropriate distinction.
"""
import unittest
import lxml
from model import String
from namespace import Xsd

class StringXsdTestCase(unittest.TestCase):



    def setUp(self):
        self.text = "xsd_text"
        self.tag = "xsd_tag"

    def tearDown(self):
        pass


    def _create_string(self, **kwargs):
        string = String(self.tag, self.text, **kwargs)
        return string

    def test_tag(self):
        s = self._create_string()
        self.assertEquals(
            "{%s}%s" % (Xsd.namespace, "element"), s.schema_node.tag
        )

    def test_nsmap(self):
        s = self._create_string()
        self.assertEquals({Xsd.prefix : Xsd.namespace}, s.schema_node.nsmap)

    def test_name(self):
        s = self._create_string()
        self.assertEquals(s.schema_node.get("name"), self.tag)

    def test_type(self):
        s = self._create_string()
        self.assertEquals(s.schema_node.get("type"), "xs:string")

    def test_default(self):
        s = self._create_string(default="default")
        self.assertEquals(s.schema_node.get("default"), "default")

    def test_fixed(self):
        s = self._create_string(default="fixed")
        self.assertEquals(s.schema_node.get("fixed"), "fixed")


    def test_enumeration(self):
#        s = self._create_string(enumeration=["A","B"])
        s = String(self.tag, "A", enumeration=["A","B"])
        print lxml.etree.tostring(s.schema_node, pretty_print=True)
        self.assertEquals(True)

    def test_length(self):
        self.assertFalse(True)

    def test_max_length(self):
        self.assertFalse(True)

    def test_min_length(self):
        self.assertFalse(True)

    def test_pattern(self):
        raise NotImplementedError

    def test_white_space(self):
        raise NotImplementedError

    

    def test_output(self):
        string = self._create_string()
        expected_xsd = '<xs:element xmlns:xs="http://www.w3.org/2001/XMLSchema" name="%s" type="xs:%s"/>' % (string.name, string.type_name)
        self.assertEquals(expected_xsd, lxml.etree.tostring(string.schema_node))