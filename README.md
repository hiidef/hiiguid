HiiGUID - Time based byte GUID
===============================

Creates a GUID based on a float so you can sort it by the GUID and maintain its order

* packed: String representing the packed struct value of the GUID.
* base36: String representing the base36 encoded value of the GUID.
* float: Float representing the non-fractional portion of the GUID's initial timestamp.

Note: Timestamps are to the nearest second.

Installation and Setup
----------------------

Installation is as easy as installing with easy_install or pip.

    >>> from hiiguid import HiiGUID
    >>> timestamp = 1315490012.0
    >>> guid = HiiGUID(timestamp).packed
    >>> unpacked_timestamp = HiiGUID(guid).timestamp
    >>> print (guid, len(guid), timestamp, unpacked_timestamp)
    ('Nh\xc8\xdc\xac\xb6\x19g\x19\xe8O)\x9a\xd9\xe9thb\xcbu', 20, 1315490012.0, 1315490012.0)
