import uuid

from pyheapfile.heap import HeapFile, to_bytes, from_bytes
from pydllfile.dllist import DoubleLinkedListFile, LINK_SIZE
from pybtreecore.btnode import Node
from pybtreecore.btnodelist import NodeList

KEYS_PER_NODE = 16

KEY_SIZE = 32
DATA_SIZE = 32


def newid():
    return uuid.uuid4().hex


class BTreeCoreFile(object):
    def __init__(self, heap_fd, alloc_max_size=None, link_size=LINK_SIZE):
        self.alloc_max_size = alloc_max_size
        self.heap_fd = heap_fd
        self.fd = DoubleLinkedListFile(heap_fd=self.heap_fd, link_size=link_size)

    def calc_empty_list(
        self,
        leaf=True,
        keys_per_node=KEYS_PER_NODE,
        key_size=KEY_SIZE,
        data_size=DATA_SIZE,
    ):
        nodelist = NodeList()
        node = Node(leaf=leaf)
        node.set_key("".join([" " for i in range(0, key_size)]))
        if leaf == True:
            node.set_data("".join([" " for i in range(0, data_size)]))
        # this nodelist is not written to heap
        # just created to get the max size on heap
        [nodelist.insert(node) for i in range(0, keys_per_node)]
        buf = nodelist.to_bytes()
        alloc_size = len(buf)
        return alloc_size

    def calc_empty(
        self,
        keys_per_node=KEYS_PER_NODE,
        key_size=KEY_SIZE,
        data_size=DATA_SIZE,
    ):
        size_leaf = self.calc_empty_list(
            leaf=True,
            keys_per_node=KEYS_PER_NODE,
            key_size=KEY_SIZE,
            data_size=DATA_SIZE,
        )
        size_inner = self.calc_empty_list(
            leaf=False,
            keys_per_node=KEYS_PER_NODE,
            key_size=KEY_SIZE,
            data_size=DATA_SIZE,
        )
        return max(size_leaf, size_inner)

    def create_empty_list(self, alloc_max_size):
        self.alloc_max_size = alloc_max_size
        node, elem, other_elem = self.fd.insert_elem(max_data_alloc=self.alloc_max_size)
        return node, elem, NodeList()

    def read_list(self, pos, free_unused=True):
        node, elem = self.fd.read_elem(pos)
        nodelist = NodeList()
        nodelist.from_bytes(elem.data)
        if free_unused == True:
            elem.data = None
        return node, elem, nodelist

    def write_list(self, node, elem, nodelist, free_unused=True):
        elem.data = nodelist.to_bytes()
        self.fd.write_elem(node, elem)
        if free_unused == True:
            elem.data = None

    def free_list(self, btlist):
        pass

    def split_list(self, btlist, pos=-1):
        pass

    def merge_list(self, btlist):
        pass
