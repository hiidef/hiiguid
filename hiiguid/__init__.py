import time
import struct
import uuid
import unittest
from random import randint, shuffle


VERSION = (0, 0, 1)


def _unpack(s):
    """Unpack a struct string into a long."""
    z = list(struct.unpack('>5I', s))
    return long(z[4] | z[3] << 32 | z[2] << 64 | z[1] << 96 | z[0] << 128)


class HiiGUID(long):

    _packed = None
    _base36 = None
    _timestamp = None

    def __new__(cls, value=time.time()):
        """
        Looks for a timestamp or string. If a timestamp, it adds the a new
        UUID4 integer. In the event of a string it attempts to decode a
        packed struct string or base36 string.
        """
        if isinstance(value, str):
            if len(value) == 20:
                value = _unpack(value)
            else:
                value = long(value, 36)
        elif isinstance(value, float):
            value = long(value) << 128 | uuid.uuid4().int
        else:
            raise ValueError("HiiGUID requires a packed struct string "
                "a base36 encoded string or a timestamp float.")
        return super(HiiGUID, cls).__new__(cls, value)

    @property
    def packed(self):
        """
        String representing the packed struct value of the GUID.
        """
        if self._packed:
            return self._packed
        words = (self >> 128, self >> 96, self >> 64, self >> 32, self)
        self._packed = struct.pack('>5I', *[x & 4294967295 for x in words])
        return self._packed

    @property
    def base36(self):
        """
        String representing the base36 encoded value of the GUID.
        """
        if self._base36:
            return self._base36
        x = self
        alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
        base36 = []
        while x:
            x, y = divmod(x, 36)
            base36.insert(0, alphabet[y])
        self._base36 = ''.join(base36)
        return self._base36

    @property
    def timestamp(self):
        """
        Float representing the non-fractional portion of the GUID's
        initial timestamp.
        """
        if self._timestamp:
            return self._timestamp
        self._timestamp = float(self >> 128)
        return self._timestamp


class HiiStartGUID(HiiGUID):

    def __new__(cls, value=time.time()):
        """
        Lowest possible value for a GUID with this timestamp.
        """
        if isinstance(value, float):
            value = long(value) << 128
            return super(HiiGUID, cls).__new__(cls, value)
        else:
            return super(HiiStartGUID, cls).__new__(cls, value)


class HiiFinishGUID(HiiGUID):

    def __new__(cls, value=time.time()):
        """
        Highest possible value for a GUID with this timestamp.
        """
        if isinstance(value, float):
            value = long(value) << 128 | 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFL
            return super(HiiGUID, cls).__new__(cls, value)
        else:
            return super(HiiFinishGUID, cls).__new__(cls, value)


class TestHiiGUID(unittest.TestCase):

    def test_packing(self):
        a = HiiGUID()
        b = HiiGUID(a.packed)
        self.assertEqual(a, b)

    def test_base36(self):
        a = HiiGUID()
        b = HiiGUID(a.base36)
        self.assertEqual(a, b)
        self.assertEqual(a.base36, b.base36)

    def test_default_timestamp(self):
        a = HiiGUID()
        b = HiiGUID(a.timestamp)
        self.assertEqual(a.timestamp, b.timestamp)
        self.assertNotEqual(a, b)

    def test_custom_timestamp(self):
        now = time.time()
        a = HiiGUID(now)
        b = HiiGUID(now)
        self.assertEqual(a.timestamp, b.timestamp)
        self.assertNotEqual(a, b)
        later = time.time() + 1
        c = HiiGUID(later)
        self.assertNotEqual(a.timestamp, c.timestamp)

    def test_chained(self):
        now = time.time()
        a = HiiGUID(now)
        b = HiiGUID(a.timestamp)
        # c = HiiGUID(b.packed)
        d = HiiGUID(b.base36)
        self.assertEqual(a.timestamp, d.timestamp)
        e = HiiGUID(now)
        self.assertEqual(d.timestamp, e.timestamp)

    def test_start_finish(self):
        now = time.time()
        start = HiiStartGUID(now)
        finish = HiiFinishGUID(now)
        self.assertTrue(start < finish)
        for i in range(0, 1000):
            a = HiiGUID(now)
            self.assertTrue(a > start)
            self.assertTrue(a < finish)


def in_order(x):
    previous = None
    for item in x:
        if previous:
            if item < previous:
                print item, previous
                return False
        previous = item
    return True


class TestHiiGUIDSorting(unittest.TestCase):

    def setUp(self):
        # Start with some random times.
        times = [time.time() + randint(0, 10000) for x in range(0, 10000)]
        # As HiiGUID is only accurate to the second, remove
        # fractional component
        times = [float(int(x)) for x in times]
        # Remove duplicate times to prevent throwing off the sorting tests
        self.times = list(set(times))
        # Shuffle the list so we can get started sorting.
        shuffle(self.times)

    def order(self, key=lambda y: y):
        guids = [(key(HiiGUID(x)), x) for x in self.times]
        guids_sorted = sorted(guids, key=lambda x: x[0])
        self.assertTrue(in_order([x[1] for x in guids_sorted]))

    def test_default_sorting(self):
        self.order()

    def test_timestamp_sorting(self):
        self.order(key=lambda x: x.timestamp)

    def test_base36_sorting(self):
        self.order(key=lambda x: x.base36)

    def test_packed_sorting(self):
        self.order(key=lambda x: x.packed)


if __name__ == '__main__':
    unittest.main()
