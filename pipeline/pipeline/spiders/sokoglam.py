# -*- coding: utf-8 -*-

"""Sokoglam Products Spider"""

# Imports =====================================================================

import json
import scrapy

from scrapy.spiders import SitemapSpider
from pipeline.items.sokoglam import ProductItem, ReviewItem, ReviewerItem
from pipeline.itemloaders.sokoglam import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class SokoglamProductsSpider(SitemapSpider):
    """Sokoglam Products Spider"""

    name = "sokoglam"
    allowed_domains = ['sokoglam.com', 'yotpo.com']
    sitemap_urls = ['https://sokoglam.com/robots.txt']
    sitemap_rules = [('/products/', 'parse_product')]
    sitemap_follow = ['/sitemap_products']

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Extract product details"""
        data = response.xpath('//script').re_first('_BISConfig.product = (.+);')
        record = json.loads(data)

        product_loader = ProductItemLoader(ProductItem(), response)
        product_loader.add_value('id', record.get('id', None))
        product_loader.add_value('sku', record.get('variants', [{}])[0].get('sku', None))
        product_loader.add_xpath('name', '//meta[@itemprop="name"]/@content')
        product_loader.add_xpath('brand', '//p[@class="vendor"]')
        product_loader.add_value('handle', record.get('handle', None))
        product_loader.add_value('type', record.get('type', None))
        product_loader.add_value('tags', record.get('tags', None))
        product_loader.add_xpath('category', '//nav[@class="breadcrumb"]/*[not(@class)]')
        product_loader.add_xpath('staffReview', '//div[@id="staff-review"]/p')
        product_loader.add_xpath('priceCurrency', '//meta[@itemprop="priceCurrency"]/@content')
        product_loader.add_xpath('price', '//meta[@itemprop="price"]/@content')
        product_loader.add_value('barcode', record.get('variants', [{}])[0].get('barcode', None))
        product_loader.add_value('inventoryQuantity', record.get('variants', [{}])[0].get('inventory_quantity', None))
        product_loader.add_value('featuredImage', record.get('featured_image', None))
        product_loader.add_value('images', record.get('images', None))
        product_loader.add_xpath('video', '//div[@id="video"]/iframe/@src')
        product_loader.add_xpath('howTo', '//div[@id="how-to"]')
        product_loader.add_xpath('keyIngredients', '//div[@id="key-ingredients"]/p')
        product_loader.add_xpath('fullIngredients', '//div[@id="full-ingredients"]/p')
        product_loader.add_xpath('availability', '//link[@itemprop="availability"]/@href')
        product_loader.add_value('description', record.get('description', None))
        product_loader.add_value('url', response.url)
        product = product_loader.load_item()        

        appkey = response.xpath('//div[@data-appkey]/@data-appkey').extract_first()
        return self.build_reviews_request(product, appkey)

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """Extract reviews data"""
        product = response.meta.get('product') or {}
        data = json.loads(response.body)
        content = scrapy.Selector(text=data[0]['result'])
        reviews = content.xpath('//div[@data-review-id]')
        if reviews:
            product['reviews'] = product.get('reviews') or []
            for each in reviews:
                # Extract review information
                review_loader = ReviewItemLoader(ReviewItem(), each)
                review_loader.add_xpath('title', './/div[contains(@class, "content-title")]')
                review_loader.add_xpath('description', './/div[contains(@class, "content-review")]')
                review_loader.add_xpath('rating', 'count(.//span[contains(@class, "yotpo-review-stars")]/span[contains(@class, "yotpo-icon-star")])')
                review_loader.add_xpath('upvotes', './/label[@data-type="up"]')
                review_loader.add_xpath('downvotes', './/label[@data-type="down"]')
                review_loader.add_xpath('datePublished', './/label[contains(@class, "yotpo-review-date")]')
                review = review_loader.load_item()

                # Extract reviewer information
                reviewer_loader = ReviewerItemLoader(ReviewerItem(), each)
                reviewer_loader.add_xpath('name', './/label[contains(@class, "yotpo-user-name")]')
                reviewer_loader.add_xpath('age', './/span[contains(@class, "yotpo-user-field-description") and contains(., "Age:")]/following-sibling::span')
                reviewer_loader.add_xpath('skinType', './/span[contains(@class, "yotpo-user-field-description") and contains(., "Skin Type:")]/following-sibling::span')
                reviewer_loader.add_xpath('verifiedBuyer', './/span[contains(@class, "yotpo-user-title")]')
                reviewer = reviewer_loader.load_item()

                review['reviewer'] = reviewer
                product['reviews'].append(review)

            appkey = response.meta['appkey']
            page = response.meta.get('page', 1) + 1
            yield self.build_reviews_request(product, appkey, page)
        else:
            yield product

    # -------------------------------------------------------------------------

    def build_reviews_request(self, product, appkey, page=1):
        """Build review request using pid and appkey"""
        data = {
            'methods': json.dumps([
                {
                    "method":"reviews",
                    "params": {
                        "page": page,
                        "host-widget":"main_widget",
                        "pid": product['id']
                    }
                }
            ]),
            'app_key': appkey,
            'is_mobile': 'false',
            'widget_version': '2017-08-14_05-17-13'
        }
        return scrapy.FormRequest(
            "https://staticw2.yotpo.com/batch",
            formdata=data,
            callback=self.parse_reviews,
            meta={
                'page': page,
                'appkey': appkey,
                'product': product
            }
        )

# END =========================================================================
