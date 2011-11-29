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

from exceptions import AttributeError

class BaseValueDescriptor(object):
    """
    """

    def __get__(self, instance, owner=None):

        if instance.fixed :
            return instance.fixed

        elif instance.default and instance._val is None :
            return instance.default

        else :
            return instance._val


    def __set__(self, instance, value):
        instance._val = value

    def __delete__(self, instance):
        instance._val = None


class StringValueDescriptor(BaseValueDescriptor):
    """
    """

    def __set__(self, instance, value):

        if instance.length :
            if len(value) != instance.length:
                raise AttributeError(
                    "Length of value is not the same a the specified length"
                )

        elif instance.max_length or instance.min_length:
            if instance.max_length and len(value) > instance.max_length:
                raise AttributeError(
                    "Length of value is greater than the specified max_length"
                )

            elif instance.max_length and instance.min_length:
                if instance.max_length < instance.min_length:
                    raise AttributeError(
                        "The max_length is less than the min_length"
                    )

            if instance.min_length and len(value) < instance.min_length:
                raise AttributeError(
                    "Length of value is less than the specified min_length"
                )

        elif instance.enumeration:
            if value not in instance.enumeration:
                raise AttributeError("value not in specified enumeration")

        super(StringValueDescriptor, self).__set__(instance, value)