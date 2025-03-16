# Scrapy settings for glamira_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging

BOT_NAME = "glamira"

SPIDER_MODULES = ["glamira_crawler.spiders"]
NEWSPIDER_MODULE = "glamira_crawler.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "glamira_crawler (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

MONGO_URI = (
    "mongodb://admin:Nguyenhaiquoc13571790@34.143.190.32:27017/?authSource=admin"
)
DB_NAME = "countly"
COLLECTION_NAME = "summary"

LOG_FILE = "app.log"
LOG_LEVEL = logging.INFO

DOWNLOAD_DELAY = 2

RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]

REDIRECT_ENABLED = True

ITEM_PIPELINES = {"glamira_crawler.pipelines.GlamiraCrawlerPipeline": 300}

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.offsite.OffsiteMiddleware": None,
}

COOKIES_ENABLED = True
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

AUTOTHROTTLE_ENABLED = False
PROXY_POOL_ENABLED = True
CONCURRENT_REQUESTS = 50
HTTPCACHE_ENABLED = True
