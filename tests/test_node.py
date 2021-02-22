import unittest

from pyheapfile.heap import HeapFile

from pybtreecore.btnode import Node


class NodeTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_node(self):
        n1 = Node(key="helloworld")
        buf = n1.to_bytes()
        n2 = Node().from_bytes(buf)
        self.assertEqual(n1, n2)

        n3 = Node(key="helloworld")
        self.assertEqual(n3, n1)
        self.assertEqual(n3, n2)

        nt = Node(key="hello world")
        self.assertNotEqual(nt, n2)

    def test_with_data(self):
        n1 = Node(key="hello", data="world")
        buf = n1.to_bytes()
        n2 = Node().from_bytes(buf)
        self.assertEqual(n1, n2)

    def test_with_links(self):
        n1 = Node(key="hello", left=1, right=2)
        buf = n1.to_bytes()
        n2 = Node().from_bytes(buf)
        self.assertEqual(n1, n2)

        self.assertEqual(n2.key, "hello")
        self.assertEqual(n2.data, None)
        self.assertEqual(n2.right, 2)
        self.assertEqual(n2.right, 2)

    def test_long_key_data(self):

        key_s = " " * 300 + "hello"
        data_s = " " * 300 + "world"

        n1 = Node(key=key_s, data=data_s)

        buf = n1.to_bytes()

        n2 = Node().from_bytes(buf)

        self.assertEqual(n1, n2)
