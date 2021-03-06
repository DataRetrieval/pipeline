# -*- coding: utf-8 -*-

"""MakingCosmetics item loaders"""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity

from pipeline.utils import clean_text

# Loaders =====================================================================

class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    sizes_out = Identity()
    category_out = Join(' ')
    documents_out = Join(', ')
    more_information_out = Join(', ')

# END =========================================================================
