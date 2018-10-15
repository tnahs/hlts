#!/usr/bin/env python

# class User defaults
IS_ADMIN = False
THEME_INDEX = 0
THEME_CHOICES = [
    ('0', 'default'),
    ('1', 'dark')
]
RESULTS_PER_PAGE = 25
RECENT_DAYS = 30

# class Annotation defaults
ORIGIN = "user"
SOURCE_PREFIX = "SRC-"
SOURCE_NONE = {
    "ID": "SRC-NONE",
    "NAME": "no source"
}
AUTHOR_PREFIX = "AUT-"
AUTHOR_NONE = {
    "ID": "AUT-NONE",
    "NAME": "no author"
}
