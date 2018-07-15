# -*- coding: utf-8 -*-

"""Ulta Products Spider"""

# Imports =====================================================================

import re
import demjson
import scrapy

from scrapy.spiders import SitemapSpider
from pipeline.items.ulta import ProductItem, ReviewItem, ReviewerItem
from pipeline.itemloaders.ulta import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class UltaProductsSpider(SitemapSpider):
    """Ulta Products Spider"""

    name = "ulta"
    allowed_domains = ['ulta.com']
    sitemap_urls = ['https://www.ulta.com/robots.txt']
    sitemap_follow = ['/detail[0-9]+.xml']
    sitemap_rules = [('product', 'parse_product')]

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Extract product details"""
        product_loader = ProductItemLoader(ProductItem(), response)
        product_loader.add_value('id', response.url, re='productId=([^&]+)')
        product_loader.add_xpath('sku', '//span[@id="itemNumber"]', re='Item #: (.+)')
        product_loader.add_xpath('name', '//h1[@itemprop="name"]')
        product_loader.add_xpath('brand', '//h2[@itemprop="brand"]')
        product_loader.add_xpath('category', '//div[@class="makeup-breadcrumb"]/ul/li/a')
        product_loader.add_xpath('category', '//div[@class="makeup-breadcrumb"]/ul/li[last()]')
        product_loader.add_css('description', '.current-longDescription')
        product_loader.add_xpath('reviewCount', '//meta[@itemprop="reviewCount"]/@content')
        product_loader.add_xpath('rating', '//meta[@itemprop="ratingValue"]/@content')
        product_loader.add_xpath('price', '//meta[@property="product:price:amount"]/@content')
        product_loader.add_xpath('priceCurrency', '//meta[@property="product:price:currency"]/@content')
        product_loader.add_xpath('image', '//meta[@itemprop="image"]/@content')
        product_loader.add_xpath('promo', '//div[@id="skuPromoText"]')
        product_loader.add_css('video', '.current-longDescription iframe::attr(src)')
        product_loader.add_css('size', '#itemSize', re='([0-9.]+)')
        product_loader.add_css('sizeUOM', '#itemSizeUOM')
        product_loader.add_css('howToUse', '.current-directions')
        product_loader.add_css('ingredients', '.current-ingredients')
        product_loader.add_css('restrictions', '.product-restriction-text')
        product_loader.add_css('hairType', '.pr-other-attribute-hairtype .pr-other-attribute-value')
        product_loader.add_css('beautyRoutine', '.pr-other-attribute-beautyroutine .pr-other-attribute-value')
        product_loader.add_css('reviewersProfile', '.pr-other-attribute-describeyourself .pr-other-attribute-value')
        product_loader.add_css('gift', '.pr-other-attribute-wasthisagift .pr-other-attribute-value')
        product_loader.add_xpath('recommendationPercentage', '//p[@class="pr-snapshot-consensus-value pr-rounded"]', re='([0-9]+)')
        product_loader.add_xpath('pros', '//div[@class="pr-snapshot-body"]//div[contains(@class, "pr-attribute-pros")]/div[@class="pr-attribute-value"]/ul/li')
        product_loader.add_xpath('cons', '//div[@class="pr-snapshot-body"]//div[contains(@class, "pr-attribute-cons")]/div[@class="pr-attribute-value"]/ul/li')
        product_loader.add_xpath('bestUses', '//div[@class="pr-snapshot-body"]//div[contains(@class, "pr-attribute-bestuses")]/div[@class="pr-attribute-value"]/ul/li')
        product_loader.add_value('url', response.url)
        product = product_loader.load_item()

        # Collect reviews if any, otherwise yield collected data
        return self.build_reviews_request(product)

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """Extract product reviews"""
        product = response.meta['product']
        if response.status == 404:
            yield product
        else:
            product['reviews'] = product.get('reviews') or []
            reviews_data = re.search('= (.+);', response.body).groups()[0]
            reviews_data = re.sub(r'\b0([0-9.]+)\b', '\\1', reviews_data)
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
            page = response.meta.get('page', 1) + 1
            yield self.build_reviews_request(product, page)

    # -------------------------------------------------------------------------

    def build_reviews_request(self, product, page=1):
        """Build request to collect reviews"""
        pid = product['id']
        encoded_pid = self.encode_pid(pid)
        url_format = 'http://www.ulta.com/reviewcenter/pwr/content/{encoded_pid}/{pid}-en_US-{page}-reviews.js'
        url = url_format.format(encoded_pid=encoded_pid, pid=pid, page=page)
        return scrapy.Request(
            url,
            callback=self.parse_reviews,
            meta={
                'product': product,
                'page': page,
                'handle_httpstatus_list': [404],
            }
        )

    # -------------------------------------------------------------------------

    @staticmethod
    def encode_pid(pid):
        """Encodes PID according to Ulta algorithm"""
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
