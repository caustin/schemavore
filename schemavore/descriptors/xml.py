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
from namespace import Xsd, primitive_nsmap

__author__ = 'chris'
class XmlInstanceElement(object):
    """
    """

    def __get__(self, instance, owner=None):

        if instance is None:
            raise ValueError(
                "This method requires an instance of the Model Class"
                )

        tag = "{%s}%s" % (Xsd.namespace, instance.name)
        element = etree.Element(tag, nsmap=primitive_nsmap)
        element.text = instance.value

        return element


class XmlNode(object):
    """Represents the XML instance element
    """

    def __get__(self, instance, owner):

        if instance is None:
            raise ValueError(
                "This Method requires an instance of the Model Class"
            )

        return etree.tostring(instance.element, pretty_print=True)