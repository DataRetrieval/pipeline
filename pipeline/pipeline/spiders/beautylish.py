# -*- coding: utf-8 -*-

"""Beautylish Products Spider"""

# Imports =====================================================================

import json
import base64
import urllib
import scrapy

from pipeline.items.beautylish import ProductItem, ReviewItem, ReviewerItem
from pipeline.itemloaders.beautylish import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class BeautylishProductsSpider(scrapy.Spider):
    """Beautylish Products Spider"""

    name = "beautylish"
    allowed_domains = ['beautylish.com']
    start_urls = ['https://www.beautylish.com/shop/browse']

    # -------------------------------------------------------------------------

    def parse(self, response):
        """Extract product links, follow them and go to next page if exists
        
        @url https://www.beautylish.com/shop/browse
        @returns requests 1
        @returns items 0 0
        """
        products = response.xpath('//a[@class="tile"]')
        for product in products:
            href = product.xpath('@href').extract_first()
            yield response.follow(href, callback=self.parse_product)

        # Follow next page if it exists
        next_page = response.xpath('//span[@class="pager_next"]/a')
        if next_page:
            href = next_page.xpath('@href').extract_first()
            yield response.follow(href)

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Extract product details
        
        @url https://www.beautylish.com/s/jeffree-star-cosmetics-holographic-makeup-bag-black
        @returns requests 1 1
        """
        encoded = response.xpath('//script').re_first('window.scriptCtx = "([^"]+)"')
        decoded = base64.b64decode(encoded)
        data = json.loads(decoded)

        product_loader = ProductItemLoader(ProductItem(), response)
        product_loader.add_xpath('gtin', '//span[@itemprop="gtin13"]')
        product_loader.add_xpath('name', '//h1[@itemprop="name"]')
        product_loader.add_xpath('brandLogo', '//h3[@itemprop="brand"]/link[@itemprop="logo"]/@href')
        product_loader.add_xpath('brand', '//h3[@itemprop="brand"]/a[@itemprop="name"]')
        product_loader.add_xpath('category', '//ul[@itemprop="breadcrumb"]/li')
        product_loader.add_xpath('rating', '//meta[@itemprop="ratingValue"]/@content')
        product_loader.add_xpath('reviewCount', '//meta[@itemprop="reviewCount"]/@content')
        product_loader.add_xpath('priceCurrency', '//meta[@itemprop="priceCurrency"]/@content')
        product_loader.add_xpath('price', '//div[@itemprop="price"]')
        product_loader.add_xpath('image', '//img[@itemprop="image"]/@src')
        product_loader.add_xpath('ingredients', '//div[@id="accord-ingredients"]')
        product_loader.add_xpath('availability', '//link[@itemprop="availability"]/@href')
        product_loader.add_xpath('shipping', '//span[@class="img"][span[contains(@class, "shipIcon_time")]]/following-sibling::div[@class="body"]')
        product_loader.add_xpath('returnPolicy', '//span[@class="img"][span[contains(@class, "shipIcon_returns")]]/following-sibling::div[@class="body"]')
        product_loader.add_xpath('description', '//div[@id="desc-accord-content"]')
        product_loader.add_value('url', response.url)
        product = product_loader.load_item()

        # Extract reviews if any, otherwise return collected data
        if product['reviewCount']:
            cipherid = data['ProductApp']['product']['cipheredId']
            return scrapy.Request(
                self.build_review_url(cipherid),
                callback=self.parse_reviews,
                meta={
                    'product': product,
                    'cipherid': cipherid,
                }
            )
            
        return product

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """Extract reviews data"""
        product = response.meta['product']
        cipherid = response.meta['cipherid']
        reviews = json.loads(response.body)
        if reviews:
            product['reviews'] = product.get('reviews') or []
            for each in reviews:
                review = self.extract_review(each)
                review['reviewer'] = self.extract_reviewer(each)
                product['reviews'].append(review)

            limit = response.meta.get('limit', 20)
            offset = response.meta.get('offset', 0) + limit
            sort = response.meta.get('sort', 'helpful')
            yield scrapy.Request(
                self.build_review_url(cipherid, offset, limit, sort),
                callback=self.parse_reviews,
                meta={
                    'product': product,
                    'cipherid': cipherid,
                    'offset': offset,
                    'limit': limit
                }
            )
        else:
            # No more reviews, yield the collected data
            yield product

    # -------------------------------------------------------------------------

    def build_review_url(self, cipherid, offset=0, limit=20, sort='helpful'):
        """Build review url from cipherid"""
        params = {
            'offset': offset,
            'limit': limit,
            'sort': sort
        }
        query = urllib.urlencode(params)
        return 'https://www.beautylish.com/rest/reviews/p-{cipherid}?{query}'.format(cipherid=cipherid, query=query)
        
    # -------------------------------------------------------------------------
    
    def extract_review(self, selector):
        """Extract review"""
        review_loader = ReviewItemLoader(ReviewItem())
        review_loader.add_value('title', selector['shortText'])
        review_loader.add_value('description', selector['text'])
        review_loader.add_value('rating', selector['rating'])
        review_loader.add_value('helpfulCount', selector['likesCount'])
        review_loader.add_value('reviewImage', selector['images'][0]['clUrl'] if selector['images'] else None)
        review_loader.add_value('datePublished', selector['isoDate'])
        return review_loader.load_item()

    # -------------------------------------------------------------------------
    
    def extract_reviewer(self, selector):
        """Extract reviewer"""
        reviewer_loader = ReviewerItemLoader(ReviewerItem())
        reviewer_loader.add_value('name', selector['userDisplayName'])
        reviewer_loader.add_value('profileUrl', selector['userUrl'])
        return reviewer_loader.load_item()
        
# END =========================================================================
