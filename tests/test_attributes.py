import unittest

import lxml

from model import Attribute, String

class DefaultAttributeTestCase(unittest.TestCase):


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

#    def test_output(self):
#        name = "name"
#        s = Attribute(name, use=True)
#
#        print lxml.etree.tostring(s.schema_node)
#        self.assertFalse(True)

class TestStringAttributeXSD(unittest.TestCase):

    def _create_string_attribute(self, name, **kwargs):
        return Attribute(name, **kwargs)

    def test_required(self):
        name="myAttributeName"
        sa = self._create_string_attribute(name, use=True)
        sn = sa.schema_node
        self.assertEqual(sn.get("use"), "required")


    def test_not_required(self):
        name ='norequired'
        sa = self._create_string_attribute(name)
        sn = sa.schema_node
        self.assertEquals(None, sn.get("use"))


    def test_name(self):
        name = "a_silly_name"
        sa = self._create_string_attribute(name)
        sn = sa.schema_node
        self.assertEqual(sn.get("name"), name)

    def test_type(self):
        name = "a_silly_name"
        sa = self._create_string_attribute(name)
        sn = sa.schema_node
        self.assertEqual('xs:string', sn.get("type"), )