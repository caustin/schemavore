import unittest
import lxml
from document import DocumentBase
from model import String


class SimpleSchemaDocument(DocumentBase):
    """
    A Simple schema with simple elements.
    """

    s1 = String("s1")
    s2 = String("s2")
    s3 = String("s3")
    s4 = String("s4")
    s5 = String("s5")
    s6 = String("s6")
    s7 = String("s7")
    s8 = String("s8")
    s9 = String("s9")
    s10 = String("s10")
    

class TestXsdDocument(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_schema_tag(self):
        xsd = SimpleSchemaDocument.get_xsd()
        order = ["s1", "s2", "s3", "s4","s5", "s6", "s7", "s8","s9", "s10"]
        root = lxml.etree.fromstring(xsd)
        rendered_order = [n.get('name') for n in root.iterchildren()]

        print order == rendered_order

        for n in root.iterchildren():
            print n.get('name')

        print lxml.etree.tostring(root, pretty_print=True)

        print xsd

        self.assertTrue(False)

    def test_xml_tag(self):
        self.assertTrue(False)

    def test_element_count(self):
        self.assertTrue(False)

    def test_type_elements(self):
        self.assertTrue(False)