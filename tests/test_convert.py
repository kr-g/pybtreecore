import unittest

from pybtreecore.conv import ConvertStr, ConvertInteger, ConvertFloat, ConvertComplex


class ConvertTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test_common(self, val, conv, **opts):
        enc = conv(**opts).encode(val)
        num = conv(**opts).decode(enc)
        self.assertEqual(num, val)

    def test_str(self):
        s = "hello world!"
        self._test_common(s, ConvertStr)

    def test_str_utf8(self):
        s = "hello world!"
        self._test_common(s, ConvertStr, encoding="utf-8")

    def test_uint(self):
        i = 1234
        self._test_common(i, ConvertInteger)

    def test_int(self):
        i = -1234
        self._test_common(i, ConvertInteger, as_unsigned=False)

    def test_float(self):
        f = 1234
        self._test_common(f, ConvertFloat, as_double=False)

    def test_double(self):
        f = 1234
        self._test_common(f, ConvertFloat, as_double=True)

    def test_complex_float(self):
        c = complex(1, 29)
        self._test_common(c, ConvertComplex, as_double=False)

    def test_complex_double(self):
        c = complex(1, 29)
        self._test_common(c, ConvertComplex, as_double=True)
