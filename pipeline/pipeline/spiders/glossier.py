# -*- coding: utf-8 -*-

"""Glossier Products Spider"""

# Imports =====================================================================

import json
import datetime

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pipeline.items.glossier import ProductItem, ReviewItem, ReviewerItem
from pipeline.itemloaders.glossier import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================


class GlossierProductsSpider(CrawlSpider):
    """Glossier Products Spider"""

    name = "glossier"
    allowed_domains = ['glossier.com', 'powerreviews.com']
    start_urls = ['https://www.glossier.com/products']
    rules = (
        # Parse product details
        Rule(
            LinkExtractor(restrict_css='.product-card-name'),
            callback='parse_product',
        ),
    )

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Extract product details

        @url https://www.glossier.com/products/milky-jelly-cleanser
        @returns requests 1 1
        """
        details = response.xpath(
            '//add-to-bag[@product]/@product').extract_first()
        if not details:
            return None
        data = json.loads(details)

        product_loader = ProductItemLoader(ProductItem(), response)
        product_loader.add_value('id', data['master'].get('id'))
        product_loader.add_value('sku', data['master'].get('sku'))
        product_loader.add_value('name', data['master'].get('name'))
        product_loader.add_css('name', '.t-h5--italic')
        product_loader.add_css('tagline', '.product-tagline')
        product_loader.add_value('price', data['master'].get('price'))
        product_loader.add_value(
            'currency', data['master'].get('display_currency')
        )
        product_loader.add_value(
            'category', data['master'].get('product_category')
        )
        product_loader.add_xpath(
            'description',
            '//div[@class="product-tagline"]/following-sibling::p[1]'
        )
        product_loader.add_xpath(
            'short_description',
            '//div[@class="product-detail-subtitle" and contains(., "What is it?")]/following-sibling::p'
        )
        product_loader.add_xpath(
            'howToUse',
            '//div[@class="product-detail-subtitle" and contains(., "How to use:")]/following-sibling::p'
        )
        product_loader.add_css('claims', '.p-prod-claims')
        product_loader.add_value(
            'options',
            [
                option['name']
                for option in data.get('option_types', [])
                if option.get('name')
            ]
        )
        product_loader.add_value(
            'images',
            [
                image['normal_ratio_url']
                for image in data['master'].get('images', [])
                if image.get('normal_ratio_url')
            ]
        )
        product_loader.add_value('videos', data.get('videos'))
        product_loader.add_xpath(
            'size',
            '//div[@class="product-tagline"]/following-sibling::p[contains(., "Size:")]',
            re=r'Size:(.+)'
        )
        product_loader.add_value('instock', data.get('can_supply'))
        product_loader.add_css('ingredients', '.modal--ingredients .o-b > p::text')

        for each in data['variants']:
            variant_loader = ProductItemLoader(ProductItem(), response)
            variant_loader.add_value('id', each.get('id'))
            variant_loader.add_value('sku', each.get('sku'))
            variant_loader.add_value('price', each.get('price'))
            variant_loader.add_value('currency', each.get('display_currency'))
            variant_loader.add_value(
                'images',
                [
                    image['normal_ratio_url']
                    for image in each.get('images', [])
                    if image.get('normal_ratio_url')
                ]
            )
            variant_loader.add_value('videos', each.get('videos'))
            variant = variant_loader.load_item()
            product_loader.add_value('variants', variant)
        product_loader.add_value('url', response.url)
        product = product_loader.load_item()

        return self.build_reviews_request(response, product)

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """Extract reviews"""
        api_key = response.meta.get('api_key')
        product = response.meta.get('product') or {}
        product['reviews'] = product.get('reviews') or []

        data = json.loads(response.body)
        if not data.get('results'):
            return product

        for each in data['results'][0]['reviews']:
            review = self.extract_review(each)
            review['reviewer'] = self.extract_reviewer(each)
            product['reviews'].append(review)

        if api_key and data['paging'].get('next_page_url'):
            return response.follow(
                data['paging']['next_page_url'],
                headers={'Authorization': api_key, 'Referer': product['url']},
                meta={
                    'product': product,
                    'api_key': api_key,
                    'handle_httpstatus_list': [404, 503]
                },
                callback=self.parse_reviews
            )

        return product

    # -------------------------------------------------------------------------

    def build_reviews_request(self, response, product):
        """Build reviews request"""
        data = response.xpath('//script[contains(., "window.Env =")]')
        data = json.loads(data.re_first(r'window\.Env = (.+)'))
        slug = response.xpath(
            '//div[@data-page_id]/@data-page_id').extract_first()
        power_reviews = data['config']['power_reviews']
        api_key = power_reviews['api_key']
        return scrapy.Request(
            'https://readservices-b2c.powerreviews.com/m/{merchant_id}/l/en_US/product/{slug}/reviews'
            .format(merchant_id=power_reviews['merchant_id'], slug=slug),
            headers={'Authorization': api_key},
            meta={
                'product': product,
                'api_key': api_key,
                'handle_httpstatus_list': [404, 503],
            },
            callback=self.parse_reviews
        )

    # -------------------------------------------------------------------------

    def extract_review(self, data):
        """Extract review information"""
        review_loader = ReviewItemLoader(ReviewItem())
        review_loader.add_value('comments', data['details']['comments'])
        review_loader.add_value('headline', data['details']['headline'])
        review_loader.add_value('rating', data['metrics']['rating'])
        review_loader.add_value(
            'datePublished',
            datetime.datetime.fromtimestamp(
                data['details']['created_date'] / 1000
            )
        )
        review_loader.add_value(
            'dateUpdated',
            datetime.datetime.fromtimestamp(
                data['details']['updated_date'] / 1000
            )
        )
        review_loader.add_value(
            'helpful_score', data['metrics']['helpful_score']
        )
        review_loader.add_value(
            'helpful_votes', data['metrics']['helpful_votes']
        )
        review_loader.add_value(
            'not_helpful_votes', data['metrics']['not_helpful_votes']
        )
        return review_loader.load_item()

    # -------------------------------------------------------------------------

    def extract_reviewer(self, data):
        """Extract reviewer information"""
        reviewer_loader = ReviewerItemLoader(ReviewerItem())
        reviewer_loader.add_value('nickname', data['details']['nickname'])
        reviewer_loader.add_value('location', data['details']['location'])
        reviewer_loader.add_value(
            'verified_buyer', data['badges']['is_verified_buyer']
        )
        reviewer_loader.add_value(
            'staff_reviewer', data['badges']['is_staff_reviewer']
        )
        reviewer_loader.add_value(
            'verified_reviewer', data['badges']['is_verified_reviewer']
        )
        return reviewer_loader.load_item()

# END =========================================================================
