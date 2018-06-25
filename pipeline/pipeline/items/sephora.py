# -*- coding: utf-8 -*-

"""Items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class BaseItem(scrapy.Item):
    """Base item"""
    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)

        # Set fields default value to None
        for field, meta in self.fields.items():
            if not self.get(field, None):
                self._values[field] = meta.get('default', None)

# -----------------------------------------------------------------------------

class ProductItem(BaseItem):
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

class ReviewItem(BaseItem):
    """Review item"""
    title = scrapy.Field()
    quickTake = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    publishedAt = scrapy.Field()
    reviewer = scrapy.Field()

# -----------------------------------------------------------------------------

class ReviewerItem(BaseItem):
    """Reviewer item"""
    name = scrapy.Field()
    skinType = scrapy.Field()
    skinTone = scrapy.Field()
    age = scrapy.Field()
    location = scrapy.Field()
    eyeColor = scrapy.Field()
    badge = scrapy.Field()

# END =========================================================================
