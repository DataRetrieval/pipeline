# -*- coding: utf-8 -*-

"""Utility functions"""

# Imports =====================================================================

import re

import six
import dateutil.parser
from parsel.utils import extract_regex
from w3lib.html import remove_tags, replace_entities

# =============================================================================

INT_REGEX = re.compile(r'(?P<extract>[+-]?\d+)', re.UNICODE)
FLOAT_REGEX = re.compile(r'(?P<extract>[+-]?(\d+([.]\d*)?|[.]\d+))', re.UNICODE)

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
    if not isinstance(text, six.string_types):
        return text

    try:
        text = re.sub(r'[\s,]*', '', text)
        return [
            float(match)
            for match in extract_regex(FLOAT_REGEX, text)
        ]
    except ValueError:
        return None

# -----------------------------------------------------------------------------

def parse_int(text):
    """Parse integer numbers"""
    if not isinstance(text, six.string_types):
        return text

    try:
        text = re.sub(r'[\s,]*', '', text)
        return [
            int(match)
            for match in extract_regex(INT_REGEX, text)
        ]
    except ValueError:
        return None

# ----------------------------------------------------------------------------

def parse_bool(text):
    """Parse booleans"""
    return text.lower() in ['true', 'yes']

# END ========================================================================
