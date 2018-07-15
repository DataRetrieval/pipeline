# -*- coding: utf-8 -*-

"""Dermstore item loaders"""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from pipeline.utils import clean_text, parse_float, parse_int, parse_date

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    category_out = Join(' > ')
    price_in = MapCompose(clean_text, parse_float)
    customersPurchased_in = MapCompose(clean_text, parse_int)
    reviewCount_in = MapCompose(clean_text, parse_int)
    ratingValue_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    reviewDate_in = MapCompose(clean_text, parse_date)

# END =========================================================================
