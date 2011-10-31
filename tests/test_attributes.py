import unittest

import lxml

from model import Attribute, String

class DefaultAttributeTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name(self):
        name = "myattribute"
        s = Attribute(name)
        self.assertEquals(name, s.name)

    def test_type(self):
        type_info = String.xsd_type_info
        s = Attribute("name")

        self.assertEquals(type_info.type_name, s.type_name)

    def test_fixed(self):
        name = "attr"
        fixed_val = "fixed"
        s = Attribute(name, fixed=fixed_val)
        self.assertEquals(fixed_val, s.fixed)

    def test_default(self):
        name = "name"
        default_val = "defdddd"
        s = Attribute(name, default=default_val)

    def test_use_true(self):
        name = "name"
        s = Attribute(name, use=True)

    def test_use_default(self):
        name = "name"
        s = Attribute(name)
        self.assertFalse(s.use)
        

    def test_namespace(self):
        # The namespace should be the ns of the type.
        #
        name = "name"
        type_info = String.xsd_type_info
        s = Attribute(name)

        self.assertEquals(type_info.namespace, s.namespace)

    def test_output(self):
        name = "name"
        s = Attribute(name)

        print lxml.etree.tostring(s.schema_node)
        self.assertFalse(True)