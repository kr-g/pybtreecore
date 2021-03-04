import unittest

from pyheapfile.heap import HeapFile

from pybtreecore.btnode import Node
from pybtreecore.conv import ConvertStr, ConvertInteger, ConvertFloat, ConvertComplex


class ConvertNodeTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_node(self):
        key = "hello_world"
        data = complex(3, 14)

        conv_key = ConvertStr()
        conv_data = ConvertComplex()

        n = Node(key=key, data=conv_data.encode(data))

        buf = n.to_bytes(encode_data=False)

        nd = Node().from_bytes(buf, decode_data=False)

        self.assertEqual(n, nd)

        cplx = conv_data.decode(nd.data)
        self.assertEqual(cplx, data)
