"""
Test the xsd generation implementation.

The current xsds are implemented as descriptors so in order to test the
implementation it is necassary to first construct an instance of a model
and then grab it's xsd attribute.  This is being tested seperatly because at
the moment is seems like an appropriate distinction.
"""
import unittest
from model import String

class StringXsdTestCase(unittest.TestCase):

    def setUp(self):
        self.text = "xsd_text"
        self.tag = "xsd_tag"

    def tearDown(self):
        pass

    def test_tag(self):
        string = String(self.tag, self.text)
        print string.xml_schema
        expected_xsd = '<xs:element name="%s" type="%s"/>' % (string.name, string.namespace)
        self.assertEquals(expected_xsd, string.xml_schema)
