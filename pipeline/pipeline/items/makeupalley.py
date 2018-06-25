# -*- coding: utf-8 -*-

"""Items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class ProductItem(scrapy.Item):
    """Product item"""
    id = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    packageQuality = scrapy.Field()
    repurchasePercentage = scrapy.Field()
    reviewCount = scrapy.Field()
    rating = scrapy.Field()
    ingredients = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    starReviewsCounts = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewItem(scrapy.Item):
    """Review item"""
    content = scrapy.Field()
    rating = scrapy.Field()
    publishedAt = scrapy.Field()
    upvotes = scrapy.Field()
    totalVotes = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(scrapy.Item):
    """Reviewer item"""
    username = scrapy.Field()
    skin = scrapy.Field()
    hair = scrapy.Field()
    eyes = scrapy.Field()
    age = scrapy.Field()
    location = scrapy.Field()
    profileUrl = scrapy.Field()

# END =========================================================================
