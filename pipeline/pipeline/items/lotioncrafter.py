# -*- coding: utf-8 -*-

"""Items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class ProductItem(scrapy.Item):
    """Product item"""
    name = scrapy.Field()
    inci = scrapy.Field()
    category = scrapy.Field()
    list_price = scrapy.Field()
    price = scrapy.Field()
    options = scrapy.Field()
    image = scrapy.Field()
    size = scrapy.Field()
    material = scrapy.Field()
    capacity = scrapy.Field()
    length = scrapy.Field()
    hlb = scrapy.Field()
    incorporation = scrapy.Field()
    appearance = scrapy.Field()
    manufacturer = scrapy.Field()
    solubility = scrapy.Field()
    country_origin = scrapy.Field()
    shipping_info = scrapy.Field()
    disclaimer = scrapy.Field()
    url = scrapy.Field()
    
# END =========================================================================
