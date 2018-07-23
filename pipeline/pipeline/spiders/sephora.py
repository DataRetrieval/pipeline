# -*- coding: utf-8 -*-

"""Sephora Products Spider"""

# Imports =====================================================================

import json

import scrapy
from scrapy.spiders import SitemapSpider

from pipeline.items.sephora import ProductItem, ReviewItem, ReviewerItem
from pipeline.itemloaders.sephora import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class SephoraProductsSpider(SitemapSpider):
    """Sephora Products Spider"""

    name = "sephora"
    allowed_domains = ['sephora.com']
    sitemap_urls = ['http://www.sephora.com/products-sitemap.xml']

    # -------------------------------------------------------------------------

    def parse(self, response):
        """Extract product details"""
        data = response.xpath('//script[@seph-json-to-js="sku"]/text()').extract_first()
        if data:
            record = json.loads(data)
            product_loader = ProductItemLoader(ProductItem(), response)
            product_loader.add_value('id', record['id'])
            product_loader.add_value('sku', record['sku_number'])
            product_loader.add_value('name', record['primary_product']['display_name'])
            product_loader.add_value('brand', record['primary_product']['brand_name'])
            product_loader.add_xpath('category', '//ol[@data-at="nav_crumb"]/li')
            product_loader.add_xpath('loveCount', '//span[@seph-love-count]/@seph-love-count')
            product_loader.add_xpath('reviewCount', '//a[@href="#pdp-reviews"]/span[@class="u-linkComplexTarget"]', re='([0-9]+)')
            product_loader.add_value('rating', record['primary_product']['rating'])
            product_loader.add_value('listPrice', record.get('list_price'))
            product_loader.add_value('valuePrice', record.get('value_price'))
            product_loader.add_value('size', record['sku_size'])
            product_loader.add_xpath('image', '//meta[@property="og:image"]/@content')
            product_loader.add_xpath('use', '//div[@id="use"]')
            product_loader.add_xpath('aboutBrand', '//div[@id="brand"]')
            product_loader.add_xpath('details', '//div[@id="details"]')
            product_loader.add_xpath('ingredients', '//div[@id="ingredients"]/p[not(@class="ng-hide")]')
            product_loader.add_value('ingredients', record['ingredients'])
            product_loader.add_xpath('shipping', '//div[@id="shipping"]/p[not(@class="ng-hide")]')
            product_loader.add_value('sephoraExclusive', record.get('is_sephora_exclusive', False))
            product_loader.add_value('url', response.url)
            product = product_loader.load_item()

            reviews_url = response.xpath('//iframe[contains(@src, "reviews.htm")]/@src').re_first('([^?]+)')
            return scrapy.Request(
                '{url}?format=embedded'.format(url=reviews_url),
                callback=self.parse_reviews,
                meta={'product': product}
            )

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """Extract reviews"""
        product = response.meta.get('product') or {}
        product['reviews'] = product['reviews'] or []
        reviews_list = response.xpath('//span[@itemprop="review"]')
        for each in reviews_list:
            review = self.extract_review(each)
            review['reviewer'] = self.extract_reviewer(each)
            product['reviews'].append(review)

        next_page = response.xpath('//a[@name="BV_TrackingTag_Review_Display_NextPage"]')
        if next_page:
            return response.follow(
                next_page.xpath('@href').extract_first(),
                callback=self.parse_reviews,
                meta={'product': product}
            )

        return product

    # -------------------------------------------------------------------------

    def extract_review(self, data):
        """Extract review information"""
        review_loader = ReviewItemLoader(ReviewItem(), data)
        review_loader.add_xpath('title', './/span[@itemprop="name"]')
        review_loader.add_xpath('quickTake', './/span[@class="BVRRTag"]')
        review_loader.add_xpath('description', './/div[@itemprop="description"]')
        review_loader.add_xpath('rating', './/span[@itemprop="ratingValue"]')
        review_loader.add_xpath('publishedAt', './/meta[@itemprop="datePublished"]/@content')
        return review_loader.load_item()

    # -------------------------------------------------------------------------

    def extract_reviewer(self, data):
        """Extract reviewer information"""
        reviewer_loader = ReviewerItemLoader(ReviewerItem(), data)
        reviewer_loader.add_xpath('name', './/span[@itemprop="author"]')
        reviewer_loader.add_xpath('skinType', './/span[contains(@class, "BVRRContextDataValueskinType") and contains(@class, "BVRRValue")]')
        reviewer_loader.add_xpath('skinTone', './/span[contains(@class, "BVRRContextDataValueskinTone") and contains(@class, "BVRRValue")]')
        reviewer_loader.add_xpath('eyeColor', './/span[contains(@class, "BVRRContextDataValueeyeColor") and contains(@class, "BVRRValue")]')
        reviewer_loader.add_xpath('age', './/span[contains(@class, "BVRRContextDataValueage") and contains(@class, "BVRRValue")]')
        reviewer_loader.add_xpath('location', './/span[contains(@class, "BVRRUserLocation") and contains(@class, "BVRRValue")]')
        reviewer_loader.add_xpath('badge', './/div[contains(@class, "BVRRReviewBadgeGraphic")]/@class', re='BVRRBadgeGraphic BVRRReviewBadgeGraphic BVRR(.+)Graphic')
        return reviewer_loader.load_item()

# END =========================================================================
