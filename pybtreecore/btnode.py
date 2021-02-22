from pyheapfile.heap import to_bytes, from_bytes

KEY_DATA_MAX = 2 ** (3 * 4)  # 4096, can be stored in 12 bits == 3 nibbles
LINK_SIZE = 8


class Node(object):
    def __init__(
        self,
        leaf=False,
        key=None,
        data=None,
        parent=0,
        left=0,
        right=0,
        link_size=LINK_SIZE,
    ):
        self.pos = 0
        self.link_size = link_size
        self.set_parent(parent)
        self.leaf = leaf
        self.set_key(key)
        self.left = left
        self.right = right
        self.set_data(data)

    def __repr__(self):
        return (
            self.__class__.__name__
            + "("
            + " leaf:"
            + str(self.leaf)
            + ", key:"
            + str(self.key)
            + ", data:"
            + str(self.data)
            + ", parent:"
            + hex(self.parent)
            + ", left:"
            + hex(self.left)
            + ", right:"
            + hex(self.right)
            + " )"
        )

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        return (
            self.leaf == other.leaf
            and self.parent_pt == other.parent_pt
            and self.key == other.key
            and self.data == other.data
            and self.parent == other.parent
            and self.left == other.left
            and self.right == other.right
        )

    def set_parent(self, xpos):
        self.parent_pt = xpos > 0
        self.parent = xpos

    def set_key(self, key):
        self.key_len = len(key) if key != None else 0
        if self.key_len > KEY_DATA_MAX:
            raise Exception("key len exceeded")
        self.key = key

    def set_data(self, data):
        self.leaf = True if data != None else False
        self.data_len = len(data) if self.leaf else 0
        if self.data_len > KEY_DATA_MAX:
            raise Exception("data len exceeded")
        self.data = data

    def to_bytes(self, encode=True):
        buf = []
        flags = 0
        if self.leaf:
            flags |= 1 << 0
        if self.parent_pt:
            flags |= 1 << 1
        buf.extend(to_bytes(flags, 1))

        key_low = self.key_len & 0xFF
        data_low = self.data_len & 0xFF

        key_high = self.key_len >> 8 & 0xF
        data_high = self.data_len >> 8 & 0xF

        high = (key_high << 4) | data_high

        buf.extend(to_bytes(high, 1))
        buf.extend(to_bytes(key_low, 1))
        buf.extend(to_bytes(data_low, 1))

        if self.key == None:
            raise Exception("no key set")

        buf.extend(self.key.encode())

        if self.parent > 0:
            if not self.parent_pt:
                raise Exception("parent pointer set")
            buf.extend(to_bytes(self.parent, self.link_size))

        if self.leaf == True:
            if self.data == None:
                raise Exception("no data set")
            if self.left != 0 or self.right != 0:
                raise Exception("link pointer set in leaf node")
            buf.extend(self.data.encode() if encode else self.data)
        else:
            if self.data != None:
                raise Exception("data set in inner node")
            buf.extend(to_bytes(self.left, self.link_size))
            buf.extend(to_bytes(self.right, self.link_size))

        return buf

    @staticmethod
    def _split(buf, blen):
        return buf[:blen], buf[blen:]

    def from_bytes(self, buf, decode=True):
        b, buf = self._split(buf, 1)
        flags = from_bytes(b)
        self.leaf = 1 << 0 & flags > 0
        self.parent_pt = 1 << 1 & flags > 0

        b, buf = self._split(buf, 1)
        high = from_bytes(b)
        key_high = high >> 4 & 0xF
        data_high = high & 0xF
        b, buf = self._split(buf, 1)
        key_low = from_bytes(b)
        b, buf = self._split(buf, 1)
        data_low = from_bytes(b)

        self.key_len = key_high << 8 | key_low
        self.data_len = data_high << 8 | data_low

        b, buf = self._split(buf, self.key_len)
        self.key = bytes(b).decode() if decode else b

        if self.parent_pt:
            b, buf = self._split(buf, self.link_size)
            self.parent = from_bytes(b)

        if self.leaf == True:
            b, buf = self._split(buf, self.data_len)
            self.data = bytes(b).decode() if decode else b
        else:
            b, buf = self._split(buf, self.link_size)
            self.left = from_bytes(b)
            b, buf = self._split(buf, self.link_size)
            self.right = from_bytes(b)

        if len(buf) > 0:
            return self, buf
        return self
