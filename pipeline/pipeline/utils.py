# -*- coding: utf-8 -*-

"""Utility functions"""

# Imports =====================================================================

import re
import datetime

import six
import dateutil.parser
from scrapy.utils.python import to_unicode
from w3lib.html import remove_tags, replace_entities

# =============================================================================

def clean_text(text):
    """Clean text from tags, replace entities and normalize whitespaces"""
    if not isinstance(text, six.string_types):
        return text
    text = remove_tags(text)
    text = replace_entities(text)
    # Normalize whitespace
    text = re.sub(r'(\s)+', '\\1', text)
    # Strip whitespace
    return text.strip()

# -----------------------------------------------------------------------------

def parse_date(text):
    """Parse dates from a string into a datetime object"""
    try:
        return dateutil.parser.parse(text)
    except ValueError:
        return None

# -----------------------------------------------------------------------------

def parse_float(text):
    """Parse float numbers"""
    try:
        if isinstance(text, six.string_types):
            text = text.replace(',', '')
        return float(text)
    except ValueError:
        return None

# -----------------------------------------------------------------------------

def parse_int(text):
    """Parse integer numbers"""
    try:
        if isinstance(text, six.string_types):
            text = text.replace(',', '')
        return int(text)
    except ValueError:
        return None

# ----------------------------------------------------------------------------

def parse_bool(text):
    """Parse booleans"""
    return text.lower() in ['true', 'yes']

# END ========================================================================
