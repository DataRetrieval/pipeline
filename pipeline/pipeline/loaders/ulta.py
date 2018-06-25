# -*- coding: utf-8 -*-

"""Item Loaders"""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity

from pipeline.utils import clean_text, parse_float, parse_int, parse_date

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    pros_out = Identity()
    cons_out = Identity()
    bestUses_out = Identity()
    category_out = Join(' > ')
    
    price_in = MapCompose(clean_text, parse_float)
    size_in = MapCompose(clean_text, parse_float)
    recommendationPercentage_in = MapCompose(clean_text, parse_int)
    reviewCount_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    pros_out = Identity()
    cons_out = Identity()
    bestUses_out = Identity()
    
    datePublished_in = MapCompose(clean_text, parse_date)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------

class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader"""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clean_text)

    skinType_out = Identity()
    bio_out = Join(', ')
    
# END =========================================================================
