# -*- coding: utf-8 -*-

"""Skinstore Products Spider"""

# Imports =====================================================================

from scrapy.spiders import SitemapSpider

from pipeline.items.skinstore import ProductItem, ReviewItem, ReviewerItem
from pipeline.itemloaders.skinstore import (
    ProductItemLoader, ReviewItemLoader, ReviewerItemLoader
)

# Spider ======================================================================

class SkinstoreProductsSpider(SitemapSpider):
    """Skinstore Products Spider"""

    name = "skinstore"
    allowed_domains = ['skinstore.com']
    sitemap_urls = ['https://www.skinstore.com/sitemapindex-product.xml.gz']
    sitemap_rules = [('/[^/]+/[0-9]+.html', 'parse_product')]

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Extract product details

        @url https://www.skinstore.com/phyto-phytoplage-rehydrating-shampoo-hair-and-body-200ml/10935700.html
        @returns items 1 1
        @returns requests 0 0
        @scrapes name brand description category price image availability ingredients
        """
        product_loader = ProductItemLoader(ProductItem(), response)
        product_loader.add_xpath('name', '//h1[@itemprop="name"]')
        product_loader.add_xpath('name', '//h1[@data-track="product-title"]')
        product_loader.add_xpath('brand', '//meta[@itemprop="brand"]/@content')
        product_loader.add_xpath('brandLogo', '//img[@data-track="product-brand-logo"]/@src')
        product_loader.add_xpath('description', '//div[@id="description"]')
        product_loader.add_css('description', '.js-prodInfo-description .content .product-info')
        product_loader.add_xpath('url', '//meta[@property="og:url"]/@content')
        product_loader.add_xpath('category', '//ul[@class="breadcrumbs_container"]/li')
        product_loader.add_xpath('reviewCount', '//meta[@itemprop="reviewCount"]/@content')
        product_loader.add_xpath('ratingValue', '//meta[@itemprop="ratingValue"]/@content')
        product_loader.add_xpath('price', '//meta[@itemprop="price"]/@content')
        product_loader.add_css('price', '.product-price')
        product_loader.add_xpath('price', '//span[@data-product-price]/@data-product-price')
        product_loader.add_xpath('priceCurrency', '//meta[@itemprop="priceCurrency"]/@content')
        product_loader.add_xpath('image', '//meta[@property="og:image"]/@content')
        product_loader.add_xpath('condition', '//meta[@itemprop="itemCondition"]/@content')
        product_loader.add_xpath('availability', '//p[@class="availability"]/span[@class="product-stock-message"]')
        product_loader.add_xpath('directions', '//th[contains(., "Directions:")]/following-sibling::td')
        product_loader.add_xpath('ingredients', '//th[contains(., "Ingredients:")]/following-sibling::td')
        product_loader.add_xpath('volume', '//th[contains(., "Volume:")]/following-sibling::td')
        product_loader.add_xpath('range', '//th[contains(., "Range:")]/following-sibling::td')
        product_loader.add_xpath('size', '//th[contains(., "Size:")]/following-sibling::td')
        product = product_loader.load_item()

        product['reviews'] = []
        reviews = response.xpath('//div[@itemprop="reviews"]')
        for each in reviews:
            review = self.extract_review(each)
            review['reviewer'] = self.extract_reviewer(each)
            product['reviews'].append(review)

        return product

    # -------------------------------------------------------------------------

    def extract_review(self, selector):
        """Extract review"""
        review_loader = ReviewItemLoader(ReviewItem(), selector)
        review_loader.add_xpath('title', './/h3[@itemprop="name"]')
        review_loader.add_xpath('description', './/p[@itemprop="description"]')
        review_loader.add_xpath('rating', './/span[@itemprop="ratingValue"]')
        review_loader.add_xpath('datePublished', './/meta[@itemprop="datePublished"]/@content')
        review_loader.add_xpath('upVotes', './/li[contains(@class, "review-yes")]/span[@class="review-number"]', re='([0-9+])')
        review_loader.add_xpath('downVotes', './/li[contains(@class, "review-no")]/span[@class="review-number"]', re='([0-9+])')
        return review_loader.load_item()

    # -------------------------------------------------------------------------

    def extract_reviewer(self, selector):
        """Extract reviewer"""
        reviewer_loader = ReviewerItemLoader(ReviewerItem(), selector)
        reviewer_loader.add_xpath('username', './/span[@itemprop="author"]')
        return reviewer_loader.load_item()

# END =========================================================================
