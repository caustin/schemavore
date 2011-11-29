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

from exceptions import ValueError, AttributeError

class NonNegativeAttributeDescriptor(object):
    """
    """

    def __init__(self, attribute_name):
        """
        @param attribute_name: The numeric attribute that should be treated as
        a Non-Negative/positve attribute
        """
        self.attribute = attribute_name

    def __get__(self, instance, owner=None):
        return getattr(instance, self.attribute)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("%s must be a positive value" % self.attribute)
        else:
            setattr(instance, self.attribute, value)


class ImmutableAttributeDescriptor(object):
    """Wraps any container that supports attribute access and enforces
    immutability on the desired attribute.

    This has been tested only with named tuples at this point
    """

    def __init__(self, attribute_name, attribute_container):
        """
        """
        self._attribute = attribute_name
        self._attribute_container = attribute_container


    def __check_container(self, instance):
        container = getattr(instance, self._attribute_container)
        if container is None :
            raise AttributeError(
                "target instance is missing 'container' attribute"
            )
        else :
            return container


    def __get__(self, instance, owner=None):
        container = self.__check_container(instance)
        attr_value = getattr(container, self._attribute)
        return attr_value


    def __set__(self, instance, value):
        self.__check_container(instance)
        raise AttributeError("can't set attribute")


    def __delete__(self, instance):
        self.__check_container(instance)
        raise AttributeError("can't delete attribute")