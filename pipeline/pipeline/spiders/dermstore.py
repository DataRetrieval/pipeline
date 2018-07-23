# -*- coding: utf-8 -*-

"""Dermstore Products Spider"""

# Imports =====================================================================

import scrapy
from scrapy.spiders import SitemapSpider

from pipeline.items.dermstore import ProductItem, ReviewItem, ReviewerItem
from pipeline.itemloaders.dermstore import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class DermstoreProductsSpider(SitemapSpider):
    """Dermstore Products Spider"""

    name = "dermstore"
    allowed_domains = ['dermstore.com']
    sitemap_urls = ['https://www.dermstore.com/robots.txt']
    sitemap_rules = [('/product_', 'parse_product')]

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Extract product details"""
        product_loader = ProductItemLoader(ProductItem(), response)
        product_loader.add_xpath('name', '//h1[@itemprop="name"]')
        product_loader.add_xpath('brand', '//h2[@itemprop="brand"]')
        product_loader.add_xpath('description', '//p[@itemprop="description"]/text()')
        product_loader.add_xpath('url', '//meta[@itemprop="url"]/@content')
        product_loader.add_xpath('category', '//ol[@class="breadcrumb"]/li')
        product_loader.add_xpath('reviewCount', '//meta[@itemprop="reviewCount"]/@content')
        product_loader.add_xpath('ratingValue', '//meta[@itemprop="ratingValue"]/@content')
        product_loader.add_xpath('price', '//meta[@itemprop="price"]/@content')
        product_loader.add_xpath('price', '//script', re='"prod_price" : "([0-9.]+)"')
        product_loader.add_xpath('image', '//img[@itemprop="image"]/@src')
        product_loader.add_xpath('customersPurchased', '//span[@class="purchCount"]', re='([0-9]+)')
        product_loader.add_xpath('details', '//div[@id="collapseDetails"]')
        product_loader.add_xpath('ingredients', '//div[@id="collapseIngredients"]')
        product_loader.add_xpath('atGlance', '//div[@id="collapseGlance"]')
        product = product_loader.load_item()

        # Extract product ID
        product_id = response.xpath('//script').re_first('prod_id: ([0-9]+)')

        # Request reviews data
        return self.reviews_request(product, product_id)

    # -------------------------------------------------------------------------

    def parse_reviews(self, response):
        """Extract reviews"""
        product = response.meta.get('product') or {}
        product['reviews'] = product.get('reviews') or []

        reviews_list = response.xpath('//div[@class="panel panel-default"]')
        for each in reviews_list:
            review = self.extract_review(each)
            reviewer_selector = each.xpath('.//div[contains(@class, "reviewer")]')
            review['reviewer'] = self.extract_reviewer(reviewer_selector)
            product['reviews'].append(review)

        # Check if there are more reviews
        if len(product['reviews']) < product['reviewCount']:
            return self.reviews_request(
                product,
                response.meta['product_id'],
                page=response.meta['page'] + 1
            )

        return product

    # -------------------------------------------------------------------------

    def reviews_request(self, product, product_id, page=1):
        """Build reviews request"""
        return scrapy.FormRequest(
            'https://www.dermstore.com/ajax/review_list.php',
            headers={'X-Requested-With': 'XMLHttpRequest'},
            formdata={
                'prod_id': str(product_id),
                'ipp': '125',
                'layout': 'dolphin',
                'page': str(page),
                'review_list_filter_type': 'skin',
                'sort': ''
            },
            callback=self.parse_reviews,
            meta={
                'product': product,
                'product_id': product_id,
                'page': page
            }
        )

    # -------------------------------------------------------------------------

    def extract_review(self, data):
        """Extract review information"""
        review_loader = ReviewItemLoader(ReviewItem(), data)
        review_loader.add_xpath('title', './/div[@class="col-sm-9"]/h5')
        review_loader.add_xpath('description', './/div[@class="col-sm-9"]/p')
        review_loader.add_xpath('rating', './/div[starts-with(@class, "starsBox")]/@class', re="star([0-9.]+)")
        return review_loader.load_item()

    # -------------------------------------------------------------------------

    def extract_reviewer(self, data):
        """Extract reviewer information"""
        reviewer_loader = ReviewerItemLoader(ReviewerItem(), data)
        reviewer_loader.add_xpath('gender', './p/strong[contains(text(), "Female") or contains(text(), "Male")]')
        reviewer_loader.add_xpath('skinType', './p/text()[contains(., "Skin Type")]/following-sibling::strong')
        reviewer_loader.add_xpath('skinTone', './p/text()[contains(., "Skin Tone")]/following-sibling::strong')
        reviewer_loader.add_xpath('age', './p/text()[contains(., "Age")]/following-sibling::strong')
        reviewer_loader.add_xpath('location', './p/text()[contains(., "from")]', re='from(.+)')
        reviewer_loader.add_xpath('reviewDate', './p[last()]/text()[last()]')
        reviewer_loader.add_xpath('isVerifiedPurchaser', './p/span[@class="highlight"]')
        return reviewer_loader.load_item()

# END =========================================================================
