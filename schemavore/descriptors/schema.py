# ----------------------------------------------------------------------------#
# schemavore - Copyright (C) schemavore contributors.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# ----------------------------------------------------------------------------#

from exceptions import ValueError
import lxml.etree as etree
import lxml
from namespace import Xsd, primitive_nsmap
SEQUENCE_TAG = "{%s}%s" % (Xsd.namespace, "sequence")

class ComplexSchemaElementNode(object):

    def __init__(self, element_name):
        self.element_name = element_name

    def __get__(self, instance, owner=None):

        tag = "{%s}%s" % (Xsd.namespace, "element")
        self.element_node = lxml.etree.Element(tag, nsmap=primitive_nsmap)
        self.element_node.set("name", instance.name)
        self.element_node.set("type", instance.type_name)

        return self.element_node


class ComplexSchemaTypeNode(object):

    def __init__(self, element_name):
        self.element_name = element_name

    def __get__(self, instance, owner=None):
        tag = "{%s}%s" % (Xsd.namespace, "complexType")
        self.element = etree.Element(tag, primitive_nsmap)
        self.element.set("name", instance.type_name)

        # Build the order indicator
        order_element = etree.SubElement(self.element, SEQUENCE_TAG)

        # Now, we need to inspect the mode and request the schema node for each
        # element contained

        cls = instance.__class__

        for node in cls.get_child_nodes():
            order_element.append(node.schema_node)

        return self.element


class ComplexXmlSchemaNode(object):

    def __init__(self, element_name="complexType"):
        self.element_name = element_name


    def __get__(self, instance, owner=None):

        # TODO: It is broken when appending a complex node it is overwriting
        # the root element.  To correct this, the schema node needs some
        # additional abstraction.  Additional design is also needed for
        # handling type style imports.
        #
        # One approach to this could be to build a wrapper (class or tuple)
        # that represents these views and return that to the client asking for
        # the schema node.
        #
        # Another, could be to add some logic to the descriptor that based on
        # values passed to the descriptor that tells it what kind of schema it
        # is.
        #
        # Yet another approach would be to implement discrete descriptors based
        # on a common ancestor that encapsulates those differences.
        #
        # <xs:element name="employee" type="personinfo"/>   <---- element_node
        #
        #<xs:complexType name="personinfo">                 <---- type_node
        #    <xs:sequence>
        #        <xs:element name="firstname" type="xs:string"/>
        #        <xs:element name="lastname"  type="xs:string"/>
        #    </xs:sequence>
        #
        #</xs:complexType>                                  <---- schema-node
        #   <ns0:complexType xmlns:ns0="mycomplex" xs="http://www.w3.org/2001/XMLSchema" name="mycomplex">
        #       <xs:sequence xmlns:xs="http://www.w3.org/2001/XMLSchema">
        #           <xs:element name="a" type="xs:string"/>
        #       </xs:sequence>
        #</ns0:complexType>


        # Build to root
        tag = "{%s}%s" % (instance.name, self.element_name)
        self.element = etree.Element(tag, primitive_nsmap)
        self.element.set("name", instance.name)

        # Build the order indicator
        order_element = etree.SubElement(self.element, SEQUENCE_TAG)

        # Now, we need to inspect the mode and request the schema node for each
        # element contained

        cls = instance.__class__

        for node in cls.get_child_nodes():
            order_element.append(node.schema_node)

        return self.element


class SimpleXmlSchemaNode(object):
    """Represents the schema node of an individual XSD element.
    """

    def __init__(self, element_name="element"):
        self.element_name = element_name


    def _build_restrictions(self, instance):
        simple_tag = "{%s}simpleType" % instance.namespace
        simple = etree.SubElement(self.element, simple_tag)
        rest_tag = "{%s}restriction" % instance.namespace
        base = "%s:%s" % (instance.prefix, instance.type_name)
        restriction = etree.SubElement(simple, rest_tag)
        restriction.set("base", base)

        return restriction


    def _build_enumeration(self, instance, restriction):
        for enum in instance.enumeration:
            etree.SubElement(
                restriction, "{%s}enumeration" % instance.namespace
            ).set("value", enum)

    def _build_length(self, instance, restriction):
        etree.SubElement(
            restriction, "{%s}length" % instance.namespace
        ).set("value", str(instance.length))


    def _build_min_max_lenth(self, instance, restriction):

        if instance.min_length:
            etree.SubElement(
                restriction, "{%s}minLength" % instance.namespace
            ).set("value", str(instance.min_length))

        if instance.max_length:
            etree.SubElement(
                restriction, "{%s}maxLength" % instance.namespace
            ).set("value", str(instance.max_length))


    def __get__(self, instance, owner=None):

        if instance.type_name is None:
            raise ValueError("type_name Must Not be None!")
        elif instance.namespace is None:
            raise ValueError("namespace must not be None.")

        tag = "{%s}%s" % (instance.namespace, self.element_name)
        self.element = etree.Element(tag, nsmap=primitive_nsmap)
        self.element.set("name", instance.name)

        if not instance.restrictions:
            self.element.set("type", "%s:%s" % (Xsd.prefix, instance.type_name))

        if instance.default:
            self.element.set('default', instance.default)
        elif instance.fixed:
            self.element.set("fixed", instance.fixed)

        # minOccurs XSD default is 1
        if instance.min_occurs != 1:
            self.element.set("minOccurs", str(instance.min_occurs))

        # maxOccurs XSD default is 1
        if instance.max_occurs != 1:
            self.element.set("maxOccurs", str(instance.max_occurs))

        if instance.restrictions:
            restriction = self._build_restrictions(instance)

            if instance.enumeration:
                self._build_enumeration(instance, restriction)

            if instance.max_length or instance.min_length:
                self._build_min_max_lenth(instance, restriction)

            if instance.length:
                self._build_length(instance, restriction)

        # handle required attributes
        if getattr(instance, "use", False):
            self.element.set("use", "required")

        return self.element