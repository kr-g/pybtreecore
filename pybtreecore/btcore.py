from pyheapfile.heap import HeapFile
from pydllfile.dllist import DoubleLinkedListFile
from pybtreecore.btnodelist import Node, NodeList


class BTreeCoreFile(object):
    def __init__(self, heapfile):
        self.fd = heapfile

    def save_list(object, btlist):
        pass

    def free_list(object, btlist):
        pass

    def split_list(object, btlist, pos=-1):
        pass

    def merge_list(object, btlist):
        pass
