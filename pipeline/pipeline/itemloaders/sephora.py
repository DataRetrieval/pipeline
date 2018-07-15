# -*- coding: utf-8 -*-

"""Sephora item loaders"""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from pipeline.utils import (
    clean_text, parse_date, parse_int, parse_float, parse_bool
)

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    category_out = Join(' > ')
    shipping_out = Join('\n')
    sephoraExclusive_in = MapCompose(clean_text, parse_bool)
    listPrice_in = MapCompose(clean_text, parse_float)
    valuePrice_in = MapCompose(clean_text, parse_float)
    loveCount_in = MapCompose(clean_text, parse_int)
    reviewCount_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    publishedAt_in = MapCompose(clean_text, parse_date)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    reviewDate_in = MapCompose(clean_text, parse_date)

# END =========================================================================
