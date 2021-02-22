import unittest

import uuid

from pybtreecore.btcore import (
    BTreeCoreFile,
    BTreeElement,
    DoubleLinkedListFile,
    HeapFile,
)
from pydllfile.dllist import Element, LINK_SIZE
from pybtreecore.btcore import Node, NodeList, newid, KEYS_PER_NODE, KEY_SIZE, DATA_SIZE

from pyheapfile.heap import Node as HeapNode

fnam = "optest.hpf"


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

        bt_elem = core.create_empty_list()
        self.assertNotEqual(bt_elem.node.id, None)

        # since the id's are unknown order is unpredictable
        bt_elem.nodelist.insert(Node(key=newid(), data="hello"))
        bt_elem.nodelist.insert(Node(key=newid(), data=" "))
        bt_elem.nodelist.insert(Node(key=newid(), data="world"))
        bt_elem.nodelist.insert(Node(key=newid(), data="!"))

        core.write_list(bt_elem)
        bt_elem2 = core.read_list(bt_elem.elem.pos)

        self.assertEqual(len(bt_elem2.nodelist), len(bt_elem.nodelist))

        for n in bt_elem2.nodelist:
            bt_elem.nodelist.remove(n)

        self.assertEqual(len(bt_elem.nodelist), 0)

        print(bt_elem2.nodelist)

        hpf.close()

    def test_other_size(self):
        hpf = HeapFile(fnam).create()
        hpf.close()

        hpf = HeapFile(fnam).open()

        node0 = hpf.alloc(0x50, data="not empty first node".encode())
        self.assertNotEqual(node0, None)

        core = BTreeCoreFile(hpf, keys_per_node=60)
        msize = core._calc_empty()

        tot_size = msize + HeapNode.node_size()

        print("total size", tot_size)
        self.assertEqual(tot_size, 2 ** 12)  # 4096 bytes

        bt_elemt = core.create_empty_list()

        hpf.close()
