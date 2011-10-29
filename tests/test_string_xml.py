import unittest
from model import String

class TestStringXmlNode(unittest.TestCase):

    def test_node_output(self):
        s = String("bob")
        s.value = "value"
        xml = s.xml_node.strip()

        print xml
        self.assertEquals('<xs:string xmlns:xs="http://www.w3.org/2001/XMLSchema">value</xs:string>', xml)

    

