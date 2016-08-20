from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.extensions.closespider
import scrapy.extensions.feedexport
import scrapy.extensions.memdebug
import scrapy.telnet
import scrapy.extensions.memusage
import scrapy.extensions.logstats
import scrapy.extensions.corestats
import scrapy.extensions.spiderstate
import scrapy.extensions.throttle
import scrapy.core.scheduler
import scrapy.core.downloader
import scrapy.core.downloader.handlers.ftp
import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory
import scrapy.core.downloader.middleware
import scrapy.middleware
import scrapy.utils.misc
from scrapy.utils.misc import load_object
from scrapy.loader import *
import scrapy.downloadermiddlewares.robotstxt
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.ajaxcrawl
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.chunked
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.decompression
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength
import scrapy.pipelines
import scrapy.pipelines.images
import scrapy.exporters
import scrapy.dupefilters
import scrapy.squeues

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
process = CrawlerProcess(get_project_settings())
process.crawl('spiderProdutos', domain='paodeacucar.com.br')
process.start() # the script will block here until the crawling is finished
