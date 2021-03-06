# -*- coding: utf-8 -*-

"""Scrapy settings for pipeline project"""

# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os

BOT_NAME = 'pipeline'

SPIDER_MODULES = ['pipeline.spiders']
NEWSPIDER_MODULE = 'pipeline.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
FAKEUSERAGENT_FALLBACK = USER_AGENT

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = int(os.getenv('SCRAPY_CONCURRENT_REQUESTS', 16))

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = float(os.getenv('SCRAPY_DOWNLOAD_DELAY', 3))
DOWNLOAD_TIMEOUT = float(os.getenv('SCRAPY_DOWNLOAD_TIMEOUT', 180))
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = int(os.getenv('SCRAPY_CONCURRENT_REQUESTS_PER_DOMAIN', 8))
CONCURRENT_REQUESTS_PER_IP = int(os.getenv('SCRAPY_CONCURRENT_REQUESTS_PER_IP', 0))

CONCURRENT_ITEMS = int(os.getenv('SCRAPY_CONCURRENT_ITEMS', 100))

# Disable cookies (enabled by default)
#COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'pipeline.pipelines.StarReviewsCounterPipeline': 300,
}

# Retry configuration
RETRY_TIMES = int(os.getenv('SCRAPY_RETRY_TIMES', 10))

RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 400, 403, 408]

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

FEED_URI = os.getenv('SCRAPY_FEED_URI')
FEED_FORMAT = os.getenv('SCRAPY_FEED_FORMAT', 'jsonlines')
