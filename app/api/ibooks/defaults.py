#!/usr/bin/env python

NS_TIME_INTERVAL_SINCE_1970 = 978307200.0
ORIGIN = "ibooks"
TAG_PREFIX = "#"
TAG_PATTERN = r"\B{prefix}[^{prefix}\s]+\s?".format(prefix=TAG_PREFIX)
COLLECTION_PREFIX = "@"
COLLECTION_PATTERN = r"\B{prefix}[^{prefix}\s]+\s?".format(prefix=COLLECTION_PREFIX)
IGNORING = {
    "underline":  True,
    "green":      False,
    "blue":       False,
    "yellow":     False,
    "pink":       False,
    "purple":     False
}