import unittest

from pybtreecore.btcore import BTreeCoreFile, DoubleLinkedListFile, HeapFile
from pydllfile.dllist import Element, LINK_SIZE
from pybtreecore.btcore import KEYS_PER_NODE, KEY_SIZE, DATA_SIZE

fnam = "mytest.hpf"


class BTreeTestCase(unittest.TestCase):
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

        inner_size = core._calc_empty_list(leaf=False)
        leaf_size = core._calc_empty_list(leaf=True)
        msize = core._calc_empty()

        n = Element(hpf)
        flag_size = 1
        key_data_len = 3

        el_size_1 = KEYS_PER_NODE * (KEY_SIZE + DATA_SIZE + flag_size + key_data_len)

        el_size_2 = KEYS_PER_NODE * (
            KEY_SIZE + 2 * LINK_SIZE + flag_size + key_data_len
        )

        print()
        print("heap list element size cls calc", msize, leaf_size, inner_size)
        print("heap list element size calc", el_size_1, el_size_2)

        self.assertEqual(msize, leaf_size)
        self.assertEqual(msize, max(el_size_1, el_size_2))

        node, elem, nodelist = core.create_empty_list()
        self.assertNotEqual(node.id, None)

        print("node id", node.id)

        hpf.close()
