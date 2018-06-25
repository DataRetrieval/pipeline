# -*- coding: utf-8 -*-

# Scrapy settings for pipeline project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'pipeline'

SPIDER_MODULES = ['pipeline.spiders']
NEWSPIDER_MODULE = 'pipeline.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Configure item pipelines
ITEM_PIPELINES = {
    'pipeline.pipelines.StarReviewsCounterPipeline': 300,
}

# Retry configuration
RETRY_TIMES = 10

HTTP_RETRY_CODES = [500, 502, 503, 504, 400, 403, 408]

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

FEED_URI = 's3://provens3/%(name)s/%(time)s.jl'
FEED_FORMAT = 'jsonlines'