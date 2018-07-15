# -*- coding: utf-8 -*-

"""Makeup Alley Products Spider"""

# Imports =====================================================================

import urllib
import scrapy

from pipeline.items.makeupalley import ProductItem, ReviewItem, ReviewerItem
from pipeline.itemloaders.makeupalley import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class MakeupAlleyProductsSpider(scrapy.Spider):
    """Makeup Alley Products Spider"""

    name = "makeupalley"
    allowed_domains = ['makeupalley.com']

    # -------------------------------------------------------------------------

    def start_requests(self):
        """Login"""
        yield scrapy.FormRequest(
            'https://www.makeupalley.com/account/login.asp',
            formdata={
                'sendtourl': 'http://www.makeupalley.com/product/',
                'UserName': 'ouahibelhanchi',
                'Password': 'MakeupAlleySpider',
                'remember': 'on',
            },
            callback=self.request_products,
            meta={'dont_cache': True}
        )

    # -------------------------------------------------------------------------

    def request_products(self, response):
        """Request products page"""
        yield scrapy.Request(
            'http://www.makeupalley.com/product/',
            meta={'dont_cache': True}
        )

    # -------------------------------------------------------------------------

    def parse(self, response):
        """Request products for each category"""
        categories = response.xpath('//select[@id="CategoryID"]/option[position() > 1]')
        for category in categories:
            category_id = category.xpath('@value').extract_first()
            params = {
                'Brand': '',
                'BrandName': '',
                'CategoryID': category_id,
                'title': ''
            }
            query = urllib.urlencode(params)
            yield scrapy.Request(
                'http://www.makeupalley.com/product/searching.asp?{query}'
                .format(query=query),
                callback=self.parse_listing,
                meta={'dont_cache': True}
            )

    # -------------------------------------------------------------------------

    def parse_listing(self, response):
        """Parse listing"""
        products = response.xpath('//div[@class="search-results"]/div/table/tr')
        for product in products:
            brand = product.xpath('.//td[1]').extract_first()
            category = product.xpath('.//td[3]').extract_first()

            href = product.xpath('.//a[contains(@href, "/product/")]/@href').extract_first()
            yield response.follow(
                href,
                callback=self.parse_product,
                meta={
                    'category': category,
                    'brand': brand,
                    'dont_cache': True
                }
            )

        # Follow next page stop until we have reached the last one
        next_page = response.xpath('//li[@class="next next-pag"]/a')
        last_page = response.xpath('//li[@class="next next-pag"]/preceding-sibling::li[2]/a[@class="active"]')
        if not last_page and next_page:
            href = next_page.xpath('@href').extract_first()
            yield response.follow(
                href,
                callback=self.parse_listing,
                meta={'dont_cache': True}
            )

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Parse product details"""
        if response.meta.get('product', None):
            product = response.meta['product']
        else:
            product_loader = ProductItemLoader(ProductItem(), response)
            product_loader.add_xpath('id', '//div[@id="ItemId"]')
            product_loader.add_xpath('name', '//div[@id="ProductName"]')
            product_loader.add_value('brand', response.meta.get('brand', None))
            product_loader.add_value('category', response.meta.get('category', None))
            product_loader.add_xpath('price', '//div[contains(@class, "product-review-stats")]/div/p[@class="price"]', re='Price:(.+)')
            product_loader.add_xpath('packageQuality', '//div[contains(@class, "product-review-stats")]/div/p[@class="pack"]', re='([0-9.]+)')
            product_loader.add_xpath('repurchasePercentage', '//div[contains(@class, "product-review-stats")]/div/p[not(span)]', re='([0-9]+)')
            product_loader.add_xpath('reviewCount', '//div[contains(@class, "product-review-stats")]/div/p/span')
            product_loader.add_xpath('rating', '//div[contains(@class, "product-review-stats")]/div/h3')
            product_loader.add_xpath('image', '//div[contains(@class, "product-image")]//img/@src')
            product_loader.add_xpath('ingredients', '//div[@id="ingredientsContent"]')
            product_loader.add_value('url', response.url)
            product = product_loader.load_item()
            product['reviews'] = []

        reviews_list = response.xpath('//div[@id="reviews-wrapper"]/div[@class="comments"]')
        for each in reviews_list:
            # Extract review information
            review_loader = ReviewItemLoader(ReviewItem(), each)
            review_loader.add_xpath('content', './/p[@class="break-word"]')
            review_loader.add_xpath('rating', './/div[@class="lipies"]/span/@class', re="l-([0-9]+)-0")
            review_loader.add_xpath('publishedAt', './/div[@class="date"]/p/text()[last()]')
            review_loader.add_xpath('upvotes', './/div[@class="thumbs"]/p', re='([0-9]+) of')
            review_loader.add_xpath('totalVotes', './/div[@class="thumbs"]/p', re='[0-9]+ of ([0-9]+)')
            review = review_loader.load_item()

            # Extract reviewer information
            reviewer_loader = ReviewerItemLoader(ReviewerItem(), each)
            reviewer_loader.context['source_url'] = response.url
            reviewer_loader.add_xpath('username', './/a[@class="track_User_Profile"]')
            reviewer_loader.add_xpath('skin', './/div[@class="important"]/p/b[contains(., "Skin")]/following-sibling::text()', re=':(.+)')
            reviewer_loader.add_xpath('hair', './/div[@class="important"]/p/b[contains(., "Hair")]/following-sibling::text()', re=':(.+)')
            reviewer_loader.add_xpath('eyes', './/div[@class="important"]/p/b[contains(., "Eyes")]/following-sibling::text()', re=':(.+)')
            reviewer_loader.add_xpath('age', './/div[@class="important"]/p/b[contains(., "Age")]/following-sibling::text()', re=':(.+)')
            reviewer_loader.add_xpath('profileUrl', './/a[@class="track_User_Profile"]/@href')
            reviewer = reviewer_loader.load_item()

            review['reviewer'] = reviewer
            product['reviews'].append(review)

        # Follow next page stop until we have reached the last one
        next_page = response.xpath('//li[@class="next next-pag"]/a')
        last_page = response.xpath('//li[@class="next next-pag"]/preceding-sibling::li[2]/a[@class="active"]')
        if not last_page and next_page:
            href = next_page.xpath('@href').extract_first()
            yield response.follow(
                href,
                callback=self.parse_product,
                meta={'product': product, 'dont_cache': True},
            )
        elif product.get('reviewCount', 0) > 0:
            # Parse user profiles if any
            # Start with first profile
            profile_url = product['reviews'][0]['reviewer']['profileUrl']
            yield response.follow(
                profile_url,
                callback=self.parse_profile,
                meta={'product': product},
                dont_filter=True
            )
        else:
            yield product

    # -------------------------------------------------------------------------

    def parse_profile(self, response):
        """Parse user profile"""
        product = response.meta['product']
        review_idx = response.meta.get('review_idx', 0)
        reviewer_loader = ReviewerItemLoader(ReviewerItem(), response)
        reviewer_loader.add_xpath('location', '//div[contains(@class, "details")]/p/b[contains(., "Location")]/following-sibling::text()')
        reviewer = reviewer_loader.load_item()
        product['reviews'][review_idx]['reviewer']['location'] = reviewer['location']

        # Parse next profile, if any
        next_review_idx = review_idx + 1
        if next_review_idx < product['reviewCount']:
            profile_url = product['reviews'][next_review_idx]['reviewer']['profileUrl']
            yield response.follow(
                profile_url,
                callback=self.parse_profile,
                meta={
                    'product': product,
                    'review_idx': next_review_idx
                },
                dont_filter=True
            )
        else:
            # Last profile, yield full product details
            yield product

# END =========================================================================
