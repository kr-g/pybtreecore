import unittest

import uuid

from pybtreecore.btcore import BTreeCoreFile, DoubleLinkedListFile, HeapFile
from pydllfile.dllist import Element, LINK_SIZE
from pybtreecore.btcore import Node, NodeList, KEYS_PER_NODE, KEY_SIZE, DATA_SIZE

fnam = "optest.hpf"


def newid():
    return uuid.uuid4().hex


class BTreeOpTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_defaults(self):
        hpf = HeapFile(fnam).create()
        hpf.close()

        hpf = HeapFile(fnam).open()

        node0 = hpf.alloc(0x50, data="not empty first node".encode())
        self.assertNotEqual(node0, None)

        core = BTreeCoreFile(hpf)

        msize = core.calc_empty()
        node, elem, nodelist = core.create_empty_list(msize)
        self.assertNotEqual(node.id, None)

        print("node id", node.id)

        # since the id's are unknown order is unpredictable
        nodelist.insert(Node(key=newid(), data="hello"))
        nodelist.insert(Node(key=newid(), data=" "))
        nodelist.insert(Node(key=newid(), data="world"))
        nodelist.insert(Node(key=newid(), data="!"))

        core.write_list(node, elem, nodelist)

        node2, elem2, nodelist2 = core.read_list(elem.pos)

        self.assertEqual(len(nodelist2), len(nodelist))

        for n in nodelist2:
            nodelist.remove(n)

        self.assertEqual(len(nodelist), 0)

        print(nodelist2)

        hpf.close()
