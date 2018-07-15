# -*- coding: utf-8 -*-

"""Skinstore items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class ProductItem(scrapy.Item):
    """Product item"""
    name = scrapy.Field()
    brand = scrapy.Field()
    brandLogo = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    priceCurrency = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    condition = scrapy.Field()
    availability = scrapy.Field()
    reviewCount = scrapy.Field()
    ratingValue = scrapy.Field()
    starReviewsCounts = scrapy.Field()
    directions = scrapy.Field()
    ingredients = scrapy.Field()
    volume = scrapy.Field()
    range = scrapy.Field()
    size = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewItem(scrapy.Item):
    """Review item"""
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    datePublished = scrapy.Field()
    upVotes = scrapy.Field()
    downVotes = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(scrapy.Item):
    """Reviewer item"""
    username = scrapy.Field()

# END =========================================================================
