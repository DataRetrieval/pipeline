# -*- coding: utf-8 -*-

"""Glossier item loaders"""

# Imports =====================================================================

from scrapy.loader import ItemLoader
from scrapy.loader.processors import (
    TakeFirst, MapCompose, Compose, Identity
)

from pipeline.utils import clean_text, parse_float, parse_int, parse_date

# Loaders =====================================================================


class ProductItemLoader(ItemLoader):
    """Product item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    options_out = Identity()
    ingredients_out = Compose(set)
    images_out = Compose(set)
    videos_out = Compose(set)
    benefits_out = Compose(set)

    variants_in = Identity()
    variants_out = Identity()

    price_in = MapCompose(clean_text, parse_float)
    reviewCount_in = MapCompose(clean_text, parse_int)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------


class ReviewItemLoader(ItemLoader):
    """Review item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    helpful_score_in = Identity()
    helpful_votes_in = Identity()
    not_helpful_votes_in = Identity()
    datePublished_in = MapCompose(clean_text, parse_date)
    dateUpdated_in = MapCompose(clean_text, parse_date)
    rating_in = MapCompose(clean_text, parse_float)

# -----------------------------------------------------------------------------


class ReviewerItemLoader(ItemLoader):
    """Reviewer item loader"""
    default_input_processor = MapCompose(clean_text)
    default_output_processor = TakeFirst()

    staff_reviewer_in = Identity()
    verified_buyer_in = Identity()
    verified_reviewer_in = Identity()

# END =========================================================================
