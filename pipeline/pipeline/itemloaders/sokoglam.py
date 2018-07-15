# -*- coding: utf-8 -*-

"""Sokoglam item loaders"""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity

from pipeline.utils import clean_text, parse_float, parse_int, parse_date

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    category_out = Join(' > ')
    images_out = Identity()
    tags_out = Identity()

    price_in = MapCompose(clean_text, parse_float)
    reviewCount_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)
    inventoryQuantity_in = MapCompose(clean_text, parse_int)

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    datePublished_in = MapCompose(clean_text, parse_date)
    rating_in = MapCompose(clean_text, parse_float)
    upvotes_in = MapCompose(clean_text, parse_int)
    downvotes_in = MapCompose(clean_text, parse_int)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

# END =========================================================================
