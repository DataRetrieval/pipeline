# -*- coding: utf-8 -*-

"""Items"""

# Imports =====================================================================

import scrapy

# Items =======================================================================

class ProductItem(scrapy.Item):
    """Product item"""
    part_number = scrapy.Field()
    name = scrapy.Field()
    cas = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    sizes = scrapy.Field()
    availability = scrapy.Field()
    inci_name = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    specifications = scrapy.Field()
    storage_shelf_life = scrapy.Field()
    ingredients = scrapy.Field()
    properties = scrapy.Field()
    use = scrapy.Field()
    appearance = scrapy.Field()
    adding_acids = scrapy.Field()
    applications = scrapy.Field()
    batch_certification = scrapy.Field()
    documents = scrapy.Field()
    more_information = scrapy.Field()
    country_origin = scrapy.Field()
    raw_material_source = scrapy.Field()
    manufacture = scrapy.Field()
    animal_testing = scrapy.Field()
    gmo = scrapy.Field()
    vegan = scrapy.Field()
    url = scrapy.Field()
    
# END =========================================================================
