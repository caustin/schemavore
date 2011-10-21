__author__ = 'chris'

from collections import namedtuple


NameSpaceMapping = namedtuple("NameSpaceTuple", "namespace prefix")
Xsd = NameSpaceMapping("http://www.w3.org/2001/XMLSchema", "xs")

# key = ns_prefix
# val = ns
primitive_nsmap = dict()
primitive_nsmap[Xsd.prefix] = Xsd.namespace
  