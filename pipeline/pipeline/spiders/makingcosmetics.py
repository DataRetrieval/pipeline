# -*- coding: utf-8 -*-

"""MakingCosmetics Products Spider"""

# Imports =====================================================================

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pipeline.items.makingcosmetics import ProductItem
from pipeline.itemloaders.makingcosmetics import ProductItemLoader

# Spider ======================================================================

class MakingCosmeticsProductsSpider(CrawlSpider):
    """MakingCosmetics Products Spider"""

    name = "makingcosmetics"
    allowed_domains = ['makingcosmetics.com']
    start_urls = [
        'https://www.makingcosmetics.com/Ingredients-A-Z_ep_1.html'
    ]
    rules = (
        # Parse product details
        Rule(
            LinkExtractor(restrict_css='.it-manu-page .mfg-name'),
            callback='parse_product',
        ),
    )

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Extract product details"""
        loader = ProductItemLoader(ProductItem(), response)
        loader.add_css('part_number', '#product_id')
        loader.add_xpath('name', '//h1[@itemprop="name"]')
        loader.add_xpath('category', '//div[@class="breadcrumbs"]//text()')
        loader.add_xpath('name', '//meta[@property="og:title"]/@content')
        loader.add_xpath('image', '//meta[@property="og:image"]/@content')
        loader.add_xpath('image', '//img[@itemprop="image"]/@src')
        loader.add_xpath('availability', '//link[@itemprop="availability"]/@href')
        loader.add_css('price', '#price')
        loader.add_css('sizes', '.dropdown-format > select > option:not(:first-child)')
        loader.add_xpath('description', '//span[@style and .="Description"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('specifications', '//span[@style and .="Specifications"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('storage_shelf_life', '//span[@style and .="Storage / Shelf Life"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('ingredients', '//span[@style and .="Ingredients"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('use', '//span[@style and .="Use"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('appearance', '//span[@style and .="Appearance"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('properties', '//span[@style and .="Properties"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('applications', '//span[@style and .="Applications"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('batch_certification', '//span[@style and .="Batch Certification"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('cas', '//span[@style and .="CAS"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('inci_name', '//span[@style and .="INCI Name"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('adding_acids', '//span[@style and .="Adding Acids"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('documents', '//span[@style and .="Documents"]/following-sibling::a[@target="_blank"]')
        loader.add_xpath('more_information', '//span[@style and .="More Information"]/following-sibling::a[@target="_blank"]')
        loader.add_xpath('country_origin', '//span[@style and .="Country of Origin"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('raw_material_source', '//span[@style and .="Raw material source"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('manufacture', '//span[@style and .="Manufacture"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('animal_testing', '//span[@style and .="Animal Testing"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('gmo', '//span[@style and .="GMO"]/following-sibling::text()', re=':(.+)')
        loader.add_xpath('vegan', '//span[@style and .="Vegan"]/following-sibling::text()', re=':(.+)')
        loader.add_value('url', response.url)
        return loader.load_item()

# END =========================================================================
