# -*- coding: utf-8 -*-

"""LotionCrafter Products Spider"""

# Imports =====================================================================

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from pipeline.items.lotioncrafter import ProductItem
from pipeline.itemloaders.lotioncrafter import ProductItemLoader

# Spider ======================================================================

class LotionCrafterProductsSpider(CrawlSpider):
    """LotionCrafter Products Spider"""

    name = "lotioncrafter"
    allowed_domains = ['lotioncrafter.com']
    start_urls = [
        'http://www.lotioncrafter.com/allproducts.php'
    ]
    rules = (
        # Parse product details
        Rule(
            LinkExtractor(restrict_css='.allProdItem'),
            callback='parse_product',
        ),
    )

    # -------------------------------------------------------------------------

    def parse_product(self, response):
        """Extract product details"""
        loader = ProductItemLoader(ProductItem(), response)
        loader.add_css('name', '.Dialog-Title-h1')
        loader.add_css('category', '.NavigationPathStatic')
        loader.add_css('list_price', '.MarketPrice > s > span')
        loader.add_css('price', '#product_price')
        loader.add_xpath('options', '//select/option[position() > 1]')
        loader.add_css('image', 'img.NoBorder::attr(src)')
        loader.add_xpath('size', '//div[@class="tabcontent"]//*[contains(., "Size:")]/following-sibling::text()')
        loader.add_xpath('inci', '//div[@class="tabcontent"]//*[contains(., "INCI:")]/following-sibling::text()')
        loader.add_xpath('hlb', '//div[@class="tabcontent"]//*[contains(., "Required HLB:")]/following-sibling::text()')
        loader.add_xpath('incorporation', '//div[@class="tabcontent"]//*[contains(., "Incorporation:")]/following-sibling::text()')
        loader.add_xpath('solubility', '//div[@class="tabcontent"]//*[contains(., "Solubility:")]/following-sibling::text()')
        loader.add_xpath('appearance', '//div[@class="tabcontent"]//*[contains(., "Appearance:")]/following-sibling::text()')
        loader.add_xpath('country_origin', '//div[@class="tabcontent"]//*[contains(., "Country of Origin:")]/following-sibling::text()')
        loader.add_xpath('manufacturer', '//div[@class="tabcontent"]//*[contains(., "Manufacturer:")]/following-sibling::text()')
        loader.add_xpath('material', '//div[@class="tabcontent"]//*[contains(., "Material:")]/following-sibling::text()')
        loader.add_xpath('capacity', '//div[@class="tabcontent"]//*[contains(., "Capacity:")]/following-sibling::text()')
        loader.add_xpath('length', '//div[@class="tabcontent"]//*[contains(., "Length:")]/following-sibling::text()')
        loader.add_xpath('shipping_info', '//div[@class="tabcontent"]//*[contains(., "Shipping Information:")]/following-sibling::text()')
        loader.add_xpath('disclaimer', '//div[@class="tabcontent"]//*[contains(., "Disclaimer")]/following-sibling::text()')
        loader.add_value('url', response.url)
        yield loader.load_item()

# END =========================================================================
