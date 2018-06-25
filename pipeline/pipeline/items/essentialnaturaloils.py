# -*- coding: utf-8 -*-

"""Items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class ProductItem(scrapy.Item):
    """Product item"""
    id = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    options = scrapy.Field()
    image = scrapy.Field()
    availability = scrapy.Field()
    reviews_count = scrapy.Field()
    reviews = scrapy.Field()
    url = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewItem(scrapy.Item):
    name = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
    rating = scrapy.Field()

# END =========================================================================
