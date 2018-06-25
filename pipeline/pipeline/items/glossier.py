# -*- coding: utf-8 -*-

"""Items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================


class ProductItem(scrapy.Item):
    """Product item"""
    id = scrapy.Field()
    sku = scrapy.Field()
    name = scrapy.Field()
    tagline = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    size = scrapy.Field()
    options = scrapy.Field()
    variants = scrapy.Field()
    short_description = scrapy.Field()
    howToUse = scrapy.Field()
    benefits = scrapy.Field()
    ingredients = scrapy.Field()
    claims = scrapy.Field()
    images = scrapy.Field()
    videos = scrapy.Field()
    instock = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    reviewCount = scrapy.Field()
    starReviewsCounts = scrapy.Field()
    url = scrapy.Field()

# -----------------------------------------------------------------------------


class ReviewItem(scrapy.Item):
    """Review item"""
    comments = scrapy.Field()
    headline = scrapy.Field()
    helpful_score = scrapy.Field()
    helpful_votes = scrapy.Field()
    not_helpful_votes = scrapy.Field()
    rating = scrapy.Field()
    datePublished = scrapy.Field()
    dateUpdated = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------


class ReviewerItem(scrapy.Item):
    """Reviewer item"""
    nickname = scrapy.Field()
    location = scrapy.Field()
    verified_reviewer = scrapy.Field()
    verified_buyer = scrapy.Field()
    staff_reviewer = scrapy.Field()

# END =========================================================================
