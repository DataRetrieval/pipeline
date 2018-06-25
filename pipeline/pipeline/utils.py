# -*- coding: utf-8 -*-

"""Utility functions"""

# Imports =====================================================================

import re
import datetime

import dateutil.parser
from w3lib.html import remove_tags, replace_entities

# =============================================================================


def clean_text(text):
    """Clean text from tags, replace entities and normalize whitespaces"""
    text = remove_tags(unicode(text))
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
        return datetime.datetime.now()

# -----------------------------------------------------------------------------


def parse_float(text):
    """Parse float numbers"""
    return float(text.replace(',', '') if text else 0)

# -----------------------------------------------------------------------------


def parse_int(text):
    """Parse int numbers"""
    return int(text.replace(',', '') if text else 0)

# ----------------------------------------------------------------------------


def parse_bool(text):
    """Parse booleans"""
    return text.lower() in ['true', 'yes']
    
# END ========================================================================
