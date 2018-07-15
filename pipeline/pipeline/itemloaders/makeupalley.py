# -*- coding: utf-8 -*-

"""Makeup Alley item loaders"""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

from pipeline.utils import clean_text, parse_int, parse_float, parse_date

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    repurchasePercentage_in = MapCompose(clean_text, parse_int)
    reviewCount_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    publishedAt_in = MapCompose(clean_text, parse_date)
    upvotes_in = MapCompose(clean_text, parse_int)
    totalVotes_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    profileUrl_in = MapCompose(clean_text)

# END =========================================================================
