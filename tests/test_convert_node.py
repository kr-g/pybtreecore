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
        data = 3.0

        conv_data = ConvertFloat()

        n = Node(key=key, data=data)

        buf = n.to_bytes(conv_data=conv_data)

        nd = Node().from_bytes(buf, conv_data=conv_data)

        self.assertEqual(n, nd)

        self.assertEqual(nd.data, data)

    def test_node_data_compl(self):
        key = "hello_world"
        data = complex(3, 14)

        conv_data = ConvertComplex()

        n = Node(key=key, data=data)

        buf = n.to_bytes(conv_data=conv_data)

        nd = Node().from_bytes(buf, conv_data=conv_data)

        self.assertEqual(n, nd)

        self.assertEqual(nd.data, data)

    def test_node_conv(self):
        key = "hello_world"
        data = complex(3, 14)

        conv_key = ConvertStr()
        conv_data = ConvertComplex()

        n = Node(key=key, data=data)

        buf = n.to_bytes(conv_key=conv_key, conv_data=conv_data)

        nd = Node().from_bytes(buf, conv_key=conv_key, conv_data=conv_data)

        self.assertEqual(n, nd)

        self.assertEqual(nd.key, key)
        self.assertEqual(nd.data, data)

    def test_node_key_conv(self):
        key = 3.14
        data = complex(3, 14)

        conv_key = ConvertFloat()
        conv_data = ConvertComplex()

        n = Node(key=key, data=data)

        buf = n.to_bytes(conv_key=conv_key, conv_data=conv_data)

        nd = Node().from_bytes(buf, conv_key=conv_key, conv_data=conv_data)

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

        n = ComplexNode(key=key, data=data)

        buf = n.to_bytes(conv_key=conv_key, conv_data=conv_data)

        nd = ComplexNode().from_bytes(buf, conv_key=conv_key, conv_data=conv_data)

        self.assertEqual(n, nd)

        self.assertEqual(nd.key, key)
        self.assertEqual(nd.data, data)

        # comparision of nodes operates on key value
        nd.key += complex(1, 1)

        self.assertGreater(nd, n)
