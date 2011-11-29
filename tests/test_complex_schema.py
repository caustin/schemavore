import unittest
import lxml
from model import ComplexModel, String


class AComplex(ComplexModel):
    one = String(name="one")
    two = String(name="two")
    three = String(name="three")

class MyComplex(ComplexModel):
    a = String(name="a")
    b = String(name="b")
    c = String(name="c")
    d = String(name="d")
    e = String(name="e")
    f = String(name="f")
    g = String(name="g")
    h = String(name="h")
    i = String(name="i")
    j = String(name="j")
    k = String(name="k")
    l = String(name="l")
    m = String(name="m")
    n = String(name="n")
    o = String(name="o")
    p = String(name="p")
    q = String(name="q")
    r = String(name="r")
    s = String(name="s")
    t = String(name="t")
    u = String(name="u")
    v = String(name="v")
    w = String(name="w")
    x = String(name="x")
    y = String(name="y")
    z = String(name="z")

    acomplex = AComplex(name="the_a_complex")


class ComplexModelTestCase(unittest.TestCase):

    def test_output(self):

        m = MyComplex(name="mycomplex")
        print lxml.etree.tostring(m.schema_node)
        self.assertTrue(False)