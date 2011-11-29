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