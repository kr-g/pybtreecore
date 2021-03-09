import unittest

from pyheapfile.heap import HeapFile

from pybtreecore.btnode import Node
from pybtreecore.btnodelist import NodeList
from pybtreecore.conv import ConvertStr, ConvertInteger, ConvertFloat, ConvertComplex


class ConvertNodeListTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_nodelist_conv(self):
        key = "hello_world"
        data = 3

        conv_key = ConvertStr()
        conv_data = ConvertFloat()

        n = Node(key=key, data=data)
        n2 = Node(key=key + "2", data=data + 2)

        nl = NodeList()
        nl.insert(n)
        nl.insert(n2)

        buf = nl.to_bytes(conv_key=conv_key, conv_data=conv_data)

        nl2 = NodeList()
        nl2.from_bytes(buf, conv_key=conv_key, conv_data=conv_data)
        self.assertEqual(len(nl), len(nl2))

        for i in range(0, len(nl2)):
            self.assertEqual(nl2[i].data, nl[i].data)
