# -*- coding: utf-8 -*-

"""Paula's Choice items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class ProductItem(scrapy.Item):
    """Product item"""
    sku = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    recommendationPercentage = scrapy.Field()
    quantity = scrapy.Field()
    image = scrapy.Field()
    reviewCount = scrapy.Field()
    concerns = scrapy.Field()
    skinTypes = scrapy.Field()
    rating = scrapy.Field()
    bestUses = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    keyIngredients = scrapy.Field()
    additionalIngredients = scrapy.Field()
    whatDoesItDo = scrapy.Field()
    howToUse = scrapy.Field()
    research = scrapy.Field()
    whyIsItDifferent = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    starReviewsCounts = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewItem(scrapy.Item):
    """Review item"""
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    datePublished = scrapy.Field()
    bottomLine = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    bestUses = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(scrapy.Item):
    """Reviewer item"""
    name = scrapy.Field()
    skinType = scrapy.Field()
    bio = scrapy.Field()
    age = scrapy.Field()
    location = scrapy.Field()

# END =========================================================================
