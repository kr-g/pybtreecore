import unittest

from pyheapfile.heap import HeapFile

from pybtreecore.btnode import Node
from pybtreecore.conv import ConvertStr, ConvertInteger, ConvertFloat, ConvertComplex


class ConvertNodeTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_node_default(self):
        key = "hello_world"
        data = complex(3, 14)

        conv_data = ConvertComplex()

        n = Node(key=key, data=conv_data.encode(data))

        buf = n.to_bytes(encode_data=False)

        nd = Node().from_bytes(buf, decode_data=False)

        self.assertEqual(n, nd)

        cplx = conv_data.decode(nd.data)
        self.assertEqual(cplx, data)

    def test_node_conv(self):
        key = "hello_world"
        data = complex(3, 14)

        conv_key = ConvertStr()
        conv_data = ConvertComplex()

        n = Node(key=key, data=data, conv_key=conv_key, conv_data=conv_data)

        buf = n.to_bytes()

        nd = Node(conv_key=conv_key, conv_data=conv_data).from_bytes(buf)

        self.assertEqual(n, nd)

        self.assertEqual(nd.key, key)
        self.assertEqual(nd.data, data)

    def test_node_key_conv(self):
        key = 3.14
        data = complex(3, 14)

        conv_key = ConvertFloat()
        conv_data = ConvertComplex()

        n = Node(key=key, data=data, conv_key=conv_key, conv_data=conv_data)

        buf = n.to_bytes()

        nd = Node(conv_key=conv_key, conv_data=conv_data).from_bytes(buf)

        self.assertEqual(n, nd)

        self.assertEqual(nd.key, key)
        self.assertEqual(nd.data, data)

    def test_node_key_complex_conv(self):

        # custom node class with __le__. refer to PEP 207 -- Rich Comparisons
        class ComplexNode(Node):
            def __lt__(self, other):
                return abs(self.key) < abs(other.key)

        key = complex(31, 4)
        data = complex(3, 14)

        conv_key = ConvertComplex()
        conv_data = ConvertComplex()

        n = ComplexNode(key=key, data=data, conv_key=conv_key, conv_data=conv_data)

        buf = n.to_bytes()

        nd = ComplexNode(conv_key=conv_key, conv_data=conv_data).from_bytes(buf)

        self.assertEqual(n, nd)

        self.assertEqual(nd.key, key)
        self.assertEqual(nd.data, data)

        # comparision of nodes operates on key value
        nd.key += complex(1, 1)

        self.assertGreater(nd, n)
