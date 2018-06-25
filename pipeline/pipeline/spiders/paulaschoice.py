# -*- coding: utf-8 -*-

"""Paula's Choice Products Spider"""

# Imports =====================================================================

import re
import demjson
import scrapy

from scrapy.spiders import SitemapSpider
from pipeline.items.paulaschoice import ProductItem, ReviewItem, ReviewerItem
from pipeline.loaders.paulaschoice import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class PaulasChoiceProductsSpider(SitemapSpider):
    """Paula's Choice Products Spider"""

    name = "paulaschoice"
    sitemap_urls = ['http://www.paulaschoice.com/robots.txt']
    sitemap_rules = [('/[^/]+/[0-9]+.html', 'parse_product')]
    
    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Extract product details"""
        product_loader = ProductItemLoader(ProductItem(), response)
        product_loader.add_xpath('sku', '//input[@id="pid"]/@value')
        product_loader.add_xpath('name', '//h1[@itemprop="name"]')
        product_loader.add_xpath('description', '//div[@itemprop="description"]')
        product_loader.add_xpath('skinTypes', '//div[@class="product-description-label" and contains(., "Skin Type:")]/following-sibling::div[@class="product-description-value"]')
        product_loader.add_xpath('concerns', '//div[@class="product-description-label" and contains(., "Concerns:")]/following-sibling::div[@class="product-description-value"]')
        product_loader.add_xpath('reviewCount', '//a[@data-element-selector=".pr-reviews"]', re='([0-9]+)')
        product_loader.add_xpath('rating', '//span[@class="pr-rating pr-rounded average"]')
        product_loader.add_xpath('recommendationPercentage', '//p[@class="pr-snapshot-consensus-value pr-rounded"]', re='([0-9]+)')
        product_loader.add_xpath('price', '//div[contains(@class, "product-select-option")]/div[@class="product-select-pricing"]', re='([0-9.]+)')
        product_loader.add_xpath('quantity', '//div[contains(@class, "product-select-option")]//div[@class="product-select-quantity"]')
        product_loader.add_xpath('quantity', '//div[@class="product-color-select-label disabled"]//div[@class="product-select-quantity"]')
        product_loader.add_xpath('price', '//div[@class="product-color-select-label disabled"]//div[@class="product-price"]', re='([0-9]+)')
        product_loader.add_xpath('image', '//img[@itemprop="image"]/@src')
        product_loader.add_xpath('keyIngredients', '//div[@class="product-additional-key-ingredients"]/a')
        product_loader.add_xpath('additionalIngredients', '//div[@class="product-additional-ingredients"]')
        product_loader.add_xpath('research', '//div[@class="product-additional-info-research"]/p')
        product_loader.add_xpath('howToUse', '//div[@class="product-info-title" and contains(., "How to use")]/following-sibling::div[@class="product-info-description"]')
        product_loader.add_xpath('whatDoesItDo', '//div[@class="product-info-title" and contains(., "What does it do?")]/following-sibling::div[@class="product-info-description"]')
        product_loader.add_xpath('whyIsItDifferent', '//div[@class="product-info-title" and contains(., "Why is it different?")]/following-sibling::div[@class="product-info-description"]')
        product_loader.add_xpath('pros', '//div[@class="pr-snapshot-body"]//div[contains(@class, "pr-attribute-pros")]/div[@class="pr-attribute-value"]/ul/li')
        product_loader.add_xpath('cons', '//div[@class="pr-snapshot-body"]//div[contains(@class, "pr-attribute-cons")]/div[@class="pr-attribute-value"]/ul/li')
        product_loader.add_xpath('bestUses', '//div[@class="pr-snapshot-body"]//div[contains(@class, "pr-attribute-bestuses")]/div[@class="pr-attribute-value"]/ul/li')
        product_loader.add_value('url', response.url)
        product = product_loader.load_item()
        product['reviews'] = []

        # Collect reviews if any, otherwise yield collected data
        yield product if not product['reviewCount'] else self.build_reviews_request(product)
        
    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """Extract product reviews"""
        product = response.meta['product']
        reviews_data = re.search('= (.+);', response.body).groups()[0]
        reviews_list = [each['r'] for each in demjson.decode(reviews_data)]
        for each in reviews_list:
            # Extract review information
            review_loader = ReviewItemLoader(ReviewItem())
            review_loader.add_value('title', each.get('h', None))
            review_loader.add_value('description', each.get('p', None))
            review_loader.add_value('rating', each.get('r', None))
            review_loader.add_value('datePublished', each.get('db', None))
            review_loader.add_value('pros', self.get_value(each.get('g', []), 'pros'))
            review_loader.add_value('cons', self.get_value(each.get('g', []), 'cons'))
            review_loader.add_value('bestUses', self.get_value(each.get('g', []), 'bestuses'))
            review_loader.add_value('bottomLine', each.get('b', {}).get('k', None))
            review = review_loader.load_item()

            # Extract reviewer information
            reviewer_loader = ReviewerItemLoader(ReviewerItem())
            reviewer_loader.add_value('name', each.get('n', None))
            reviewer_loader.add_value('skinType', self.get_value(each.get('g', []), 'skintype'))
            reviewer_loader.add_value('bio', self.get_value(each.get('g', []), 'describeyourself'))
            reviewer_loader.add_value('age', self.get_value(each.get('g', []), 'age'))
            reviewer_loader.add_value('location', each['w'])
            reviewer = reviewer_loader.load_item()

            review['reviewer'] = reviewer
            product['reviews'].append(review)

        # Collect more reviews if any
        if len(product['reviews']) < product['reviewCount']:
            page = response.meta['page'] + 1
            yield self.build_reviews_request(product, page)
        else:
            yield product
     
    # -------------------------------------------------------------------------
    
    def build_reviews_request(self, product, page=1):
        """Build request to collect reviews"""
        pid = product['sku'].split('-')[0]
        encoded_pid = self.encode_pid(pid)
        url_format = 'http://www.paulaschoice.com/on/demandware.static/-/Sites-pc-catalog-nav/en_US/v1502744640485/pwr/content/{encoded_pid}/{pid}-en_US-{page}-reviews.js'
        url = url_format.format(encoded_pid=encoded_pid, pid=pid, page=page)
        return scrapy.Request(
            url,
            callback=self.parse_reviews,
            meta={
                'product': product,
                'page': page
            }
        )
        
    # -------------------------------------------------------------------------
    
    @staticmethod
    def encode_pid(pid):
        """Encodes PID according to Paula's choice algorithm"""
        result = str(sum(ord(char) * abs(255 - ord(char)) for char in pid) % 1023)
        while len(result) % 4 != 0:
            result = '0' + result
        parts = [result[i:i+2] for i in xrange(0, len(result), 2)]
        return '/'.join(parts)

    # -------------------------------------------------------------------------

    @staticmethod
    def get_value(data, needle, key='k', value='v'):
        """Get value that match key"""
        for each in data:
            try:
                if each.get(key, '').lower() == needle.lower():
                    return each[value]
            except AttributeError:
                pass
        return None
        
# END =========================================================================
