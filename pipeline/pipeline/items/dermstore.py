# -*- coding: utf-8 -*-

"""Items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class ProductItem(scrapy.Item):
    """Product item"""
    name = scrapy.Field()
    brand = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    category = scrapy.Field()
    customersPurchased = scrapy.Field()
    reviewCount = scrapy.Field()
    ratingValue = scrapy.Field()
    starReviewsCounts = scrapy.Field()
    atGlance = scrapy.Field()
    details = scrapy.Field()
    ingredients = scrapy.Field()
    url = scrapy.Field()
    reviews = scrapy.Field()
    
# -----------------------------------------------------------------------------

class ReviewItem(scrapy.Item):
    """Review item"""
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    reviewer = scrapy.Field()
    
# -----------------------------------------------------------------------------

class ReviewerItem(scrapy.Item):
    """Reviewer item"""
    gender = scrapy.Field()
    skinType = scrapy.Field()
    skinTone = scrapy.Field()
    age = scrapy.Field()
    location = scrapy.Field()
    reviewDate = scrapy.Field()
    isVerifiedPurchaser = scrapy.Field()
    
# END =========================================================================
