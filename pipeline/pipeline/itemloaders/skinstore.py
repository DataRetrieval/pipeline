# -*- coding: utf-8 -*-

"""Skinstore item loaders"""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from pipeline.utils import clean_text, parse_date, parse_float, parse_int

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    category_out = Join(' > ')
    price_in = MapCompose(clean_text, parse_float)
    reviewCount_in = MapCompose(clean_text, parse_int)
    ratingValue_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    upVotes_in = MapCompose(clean_text, parse_int)
    downVotes_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)
    datePublished_in = MapCompose(clean_text, parse_date)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

# END =========================================================================
