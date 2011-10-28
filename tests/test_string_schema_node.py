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
        self.text = "text"
        self.tag = "tag"
        self.string = None

    def tearDown(self):
        self.string = None


    def _create_string(self, tag="tag", text="text", **kwargs):
        self.string = String(tag, text, **kwargs)

    def test_tag(self):
        self._create_string()
        self.assertEquals(
            "{%s}%s" % (Xsd.namespace, "element"), self.string.schema_node.tag
        )

    def test_nsmap(self):
        self._create_string()
        self.assertEquals({Xsd.prefix : Xsd.namespace}, self.string.schema_node.nsmap)

    def test_name(self):
        self._create_string()
        self.assertEquals(self.string.schema_node.get("name"), self.tag)

    def test_type(self):
        self._create_string()
        self.assertEquals(self.string.schema_node.get("type"), "xs:string")

    def test_default(self):
        self._create_string(default="default")
        self.assertEquals(self.string.schema_node.get("default"), "default")

    def test_fixed(self):
        self._create_string(fixed="fixed")
        self.assertEquals(self.string.schema_node.get("fixed"), "fixed")


    def test_enumeration_length(self):
        enum = ["A","B"]
        self._create_string(text="A",enumeration=enum)
        sn = self.string.schema_node
        en_vals = [node.get("value") for node in sn.iter("{http://www.w3.org/2001/XMLSchema}enumeration")]

        for e in enum:
            self.assertTrue(e in en_vals)


    def test_enumeration_content(self):
        enum = ["A","B"]
        self._create_string(text="A", enumeration=enum)
        sn = self.string.schema_node
        en_vals = [node.get("value") for node in sn.iter("{http://www.w3.org/2001/XMLSchema}enumeration")]

        for e in enum:
            self.assertTrue(e in en_vals)


    def test_length_count(self):
        self._create_string("tag", "123456", length=6)
        lengths = [node for node in self.string.schema_node.iter("{http://www.w3.org/2001/XMLSchema}length")]
        self.assertEquals(1, len(lengths))

    def test_length_value(self):
        len = 6
        self._create_string("tag", "123456", length=len)
        lengths = [node.get("value") for node in self.string.schema_node.iter("{http://www.w3.org/2001/XMLSchema}length")]
        self.assertEquals(len, int(lengths[0]))


    def test_max_length_count(self):
        max_length = 6
        self._create_string("tag", "123456", max_length=max_length)
        lengths = [node for node in self.string.schema_node.iter("{http://www.w3.org/2001/XMLSchema}maxLength")]
        self.assertEquals(1, len(lengths))

    def test_max_length_value(self):
        len = 6
        self._create_string("tag", "123456", max_length=len)
        max_lens = [node.get("value") for node in self.string.schema_node.iter("{http://www.w3.org/2001/XMLSchema}maxLength")]
        self.assertEquals(len, int(max_lens[0]))


    def test_min_length_value(self):
        len = 6
        self._create_string("tag", "123456", min_length=len)
        max_lens = [node.get("value") for node in self.string.schema_node.iter("{http://www.w3.org/2001/XMLSchema}minLength")]
        self.assertEquals(len, int(max_lens[0]))

    def test_min_length_count(self):
        min_length = 6
        self._create_string("tag", "123456", min_length=min_length)
        lengths = [node for node in self.string.schema_node.iter("{http://www.w3.org/2001/XMLSchema}minLength")]
        self.assertEquals(1, len(lengths))



    def test_pattern(self):
        raise NotImplementedError

    def test_white_space(self):
        raise NotImplementedError

    def test_output(self):
        self._create_string()
        expected_xsd = '<xs:element xmlns:xs="http://www.w3.org/2001/XMLSchema" name="%s" type="xs:%s"/>' % (self.string.name, self.string.type_name)
        self.assertEquals(expected_xsd, lxml.etree.tostring(self.string.schema_node))