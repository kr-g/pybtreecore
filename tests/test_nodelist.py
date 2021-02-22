import unittest

from pyheapfile.heap import HeapFile

from pybtreecore.btnodelist import Node, NodeList


class NodeListTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def the_nodelist(self):
        n1 = Node(key="hello", left=1, right=2)
        n2 = Node(key="world", left=3, right=4)
        n3 = Node(key="leaf1", data="hello")
        n4 = Node(key="leaf2", data="world")

        nl = NodeList()
        nl.insert(n1).insert(n2).insert(n3).insert(n4)
        return nl, n1, n2, n3, n4

    def test_nodelist(self):
        nl, n1, n2, n3, n4 = self.the_nodelist()

        buf = nl.to_bytes()

        li = NodeList().from_bytes(buf)

        n__3 = li[3]
        self.assertEqual(n2, n__3)

        org = set(map(lambda x: x.key, nl.arr))
        comp = set(["hello", "world", "leaf1", "leaf2"])
        self.assertEqual(org, comp)

        self.assertEqual(n1, nl[0])
        self.assertEqual(n3, nl[1])
        self.assertEqual(n4, nl[2])
        self.assertEqual(n2, nl[3])

    def test_nodelist_remove(self):
        nl, n1, n2, n3, n4 = self.the_nodelist()

        nl.remove(n1)
        self.assertEqual(3, len(nl))

        self.assertEqual(n3, nl[0])
        self.assertEqual(n4, nl[1])
        self.assertEqual(n2, nl[2])

    def test_nodelist_pop(self):
        nl, n1, n2, n3, n4 = self.the_nodelist()

        nl.pop(1)
        self.assertEqual(3, len(nl))

        self.assertEqual(n1, nl[0])
        self.assertEqual(n4, nl[1])
        self.assertEqual(n2, nl[2])

    def test_nodelist_split_join(self):
        nli, n1, n2, n3, n4 = self.the_nodelist()

        nl = nli[:2]
        nr = nli[2:]

        self.assertEqual(n1, nl[0])
        self.assertEqual(n3, nl[1])

        self.assertEqual(n4, nr[0])
        self.assertEqual(n2, nr[1])

        ng = nl + nr
        self.assertEqual(nli, ng)

        self.assertEqual(n1, ng[0])
        self.assertEqual(n3, ng[1])
        self.assertEqual(n4, ng[2])
        self.assertEqual(n2, ng[3])

    def test_nodelist_key_data(self):
        nl, n1, n2, n3, n4 = self.the_nodelist()

        keys = nl.keys()
        data = nl.values()

        self.assertEqual(len(keys), 2)
        self.assertEqual(keys, ["leaf1", "leaf2"])
        self.assertEqual(data, ["hello", "world"])
