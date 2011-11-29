import lxml
from model import String, ModelBase

class DocumentBase(object):
    """Represents a XML or XSD document
    """

    # -------------------- Class Attributes --------------------------------- #
    namespace = None

    # -------------------- class / static methods --------------------------- #
    @classmethod
    def get_xsd(cls):
        nodes = dict()
        # TODO: Optimize the nsmap imports
        document = lxml.etree.Element(
            "{%s}%s" % ('http://www.w3.org/2001/XMLSchema', 'schema'),
            nsmap={"xs":'http://www.w3.org/2001/XMLSchema'}
        )

        for key, value in cls.__dict__.iteritems():
            if issubclass(value.__class__, ModelBase):
                nodes[key] = value

        if len(nodes.keys()) > 0:
            for key, val in sorted(
                    nodes.items(),key=lambda (key, val):
                    (val.creation_counter, key)):

                document.append(val.schema_node)

        return lxml.etree.tostring(
            document,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8'
        )

    @classmethod
    def get_wsdl(cls):
        """
        """
        pass

    def __setattr__(self, key, value):

        # Overriding to implement a default attribute for the elements
        attr = getattr(self, key, None)

        if attr:
            if issubclass(attr.__class__, ModelBase):
                attr.value = value

        super(DocumentBase, self).__setattr__(key, value)


class MyDocument(DocumentBase):
    """This is a doc string.
    """

    s1 = String("s1", enumeration=['val', 'sal'])
    s2 = String("s2", max_length=6, min_length=4)
    s3 = String("s3", length=3, default="123")
    s4 = String("s4", fixed="a")
    s5 = String('s5')