# -*- coding: utf-8 -*-

"""Item Loaders"""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity

from pipeline.utils import clean_text, parse_float, parse_int

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    rating_in = MapCompose(float)
    reviews_count_in = MapCompose(clean_text, parse_int)

    category_out = Join(' > ')
    options_out = Identity()

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    rating_in = MapCompose(parse_float)

# END =========================================================================
