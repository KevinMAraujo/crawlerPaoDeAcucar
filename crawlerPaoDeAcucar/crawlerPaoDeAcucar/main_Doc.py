from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess
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
import logging
from tkinter import *
import sys

def main():
    logging.basicConfig(filename='logExecucao.log', level=logging.INFO)
    logging.info("Started")
    #configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    print(logging.info("#### Iniciando script #### \n"))
    print("##########")
    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl('spiderProdutos', domain='paodeacucar.com.br')
    d.addBoth(lambda _: reactor.stop())
    print(logging.info("##### Processo de crawler iniciado. \nAguarde o termino do processo...."))
    reactor.run()
    #logging.info(reactor.run())
    print(logging.info("\n\n##### O processo crawler terminou."))
    logging.info('Finished')

if __name__ == '__main__':
    main()