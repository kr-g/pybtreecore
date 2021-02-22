import bisect

from .btnode import Node


class NodeList(object):
    def __init__(self, pos=0):
        self.pos = pos
        self.arr = []

    def insert(self, o):
        bisect.insort_right(self.arr, o)
        return self

    def sort(self):
        self.arr.sort()

    def pop(self, pos=-1):
        return self.arr.pop(pos)

    def remove(self, o):
        return self.arr.remove(o)

    def find_key(self, key):
        for i in len(self.arr):
            skey = self[i].key
            if skey == key:
                return i
            if skey > key:
                break
        return -1

    def keys(self):
        return list(self._keys())

    def _keys(self):
        return map(lambda x: x.key, filter(lambda x: x.leaf, self.arr))

    def values(self):
        return self._values()

    def _values(self):
        return list(map(lambda x: x.data, filter(lambda x: x.leaf, self.arr)))

    def __len__(self):
        return len(self.arr)

    def __getitem__(self, pos):
        return self.arr[pos]

    def __contains__(self, key):
        return key in self._keys()

    def __eq__(self, other):
        size = len(self)
        if size != len(other):
            return False
        for i in range(0, size):
            if self[i] != other[i]:
                return False
        return True

    def to_bytes(self):
        buf = []
        _len = len(self.arr)
        if _len > 0xFF:
            raise Exception("too much nodes in list")
        for i in range(0, _len):
            obj = self.arr[i]
            if not isinstance(obj, Node):
                raise Exception("wrong object")
            buf.extend(obj.to_bytes())
        return buf

    @staticmethod
    def _split(buf, blen):
        return buf[:blen], buf[blen:]

    def from_bytes(self, buf):
        while len(buf) > 0:
            n = Node()
            res = n.from_bytes(buf)
            self.arr.append(n)
            if isinstance(res, Node):
                break
            _, buf = res
        return self
