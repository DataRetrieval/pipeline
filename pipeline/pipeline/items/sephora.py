# -*- coding: utf-8 -*-

"""Sephora items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class ProductItem(scrapy.Item):
    """Product item"""
    id = scrapy.Field()
    sku = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    listPrice = scrapy.Field()
    valuePrice = scrapy.Field()
    size = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    loveCount = scrapy.Field()
    reviewCount = scrapy.Field()
    rating = scrapy.Field()
    use = scrapy.Field()
    details = scrapy.Field()
    aboutBrand = scrapy.Field()
    ingredients = scrapy.Field()
    shipping = scrapy.Field()
    sephoraExclusive = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    starReviewsCounts = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewItem(scrapy.Item):
    """Review item"""
    title = scrapy.Field()
    quickTake = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    publishedAt = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(scrapy.Item):
    """Reviewer item"""
    name = scrapy.Field()
    skinType = scrapy.Field()
    skinTone = scrapy.Field()
    age = scrapy.Field()
    location = scrapy.Field()
    eyeColor = scrapy.Field()
    badge = scrapy.Field()

# END =========================================================================
