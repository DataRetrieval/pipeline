# -*- coding: utf-8 -*-

"""Beautylish items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class ProductItem(scrapy.Item):
    """Product item"""
    gtin = scrapy.Field()
    name = scrapy.Field()
    brandLogo = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    priceCurrency = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    reviewCount = scrapy.Field()
    rating = scrapy.Field()
    ingredients = scrapy.Field()
    availability = scrapy.Field()
    shipping = scrapy.Field()
    returnPolicy = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    starReviewsCounts = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewItem(scrapy.Item):
    """Review item"""
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    helpfulCount = scrapy.Field()
    reviewImage = scrapy.Field()
    datePublished = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(scrapy.Item):
    """Reviewer item"""
    name = scrapy.Field()
    profileUrl = scrapy.Field()

# END =========================================================================
