# -*- coding: utf-8 -*-

"""LotionCrafter item loaders"""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity

from pipeline.utils import clean_text

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    options_out = Identity()

# END =========================================================================
