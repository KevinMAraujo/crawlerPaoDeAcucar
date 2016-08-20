# -*- coding: utf-8 -*-
import os, re, csv, json, scrapy, logging
from scrapy.http import Request
#from scrapy.conf import settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
#from ..items import CrawlerpaodeacucarItem
from scrapy.exporters import CsvItemExporter
from scrapy.utils.log import configure_logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.crawler import Crawler
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from scrapy import log, signals, Spider, Item, Field
from scrapy.settings import Settings

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)
def strip_and_join(values):
    if len(values)>0:
        value = values[0].strip()
        joined = u' '.join(value.split('\n'))
        joined = joined.replace('\r', '').replace('(', '').replace(')','')
        joined = joined.replace(u'\xc0','a').replace(u'\xc1','a').replace(u'\xc2','a').replace(u'\xc3','a').replace(u'\xc4','a').replace(u'\xe0','a').replace(u'\xe1','a').replace(u'\xe2','a').replace(u'\xe3','a').replace(u'\xe4','a')
        joined = joined.replace(u'\xca','e').replace(u'\xc8','e').replace(u'\xc9','e').replace(u'\xe8','e').replace(u'\xe9','e').replace(u'\xea','e')
        joined = joined.replace(u'\xcd','i').replace(u'\xed','i').replace(u'\xee','i').replace(u'\xef','i').replace(u'\xce','i')
        joined = joined.replace(u'\xd2','o').replace(u'\xd3','o').replace(u'\xd4','o').replace(u'\xf2','o').replace(u'\xf3','o').replace(u'\xf4','o').replace(u'\xf5','o').replace(u'\xf6','o')
        joined = joined.replace(u'\xda','u').replace(u'\xdc','u').replace(u'\xd9','u').replace(u'\xf9','u').replace(u'\xfa','u').replace(u'\xfb','u').replace(u'\xfc','u')
        joined = joined.replace(u'\xc7','c').replace(u'\xe7','c').replace(u'\xd1','n').replace(u'\xd5','c').replace(u'\xb0','')
        joined = joined.replace(u'\u2019',"'").replace(u'\u014d','o').replace(u'\u0101','a')
        joined = joined.replace(u'\xa0',' ')
        joined = joined.replace(u'\xba','').replace(u'\xb4','').replace(u'\xb7','').replace(u'\xbf','').replace(u'\x88','')
        joined = joined.replace(u'\xb2','2').replace(u'\xf1','n').replace(u'\xa5','y')
        return joined
    else:
        return u'0'
# define os itens da classe
class CrawlerpaodeacucarItem(scrapy.Item):
    nome = scrapy.Field(serializer=strip_and_join)
    id = scrapy.Field()
    preco = scrapy.Field()
    categorias1 = scrapy.Field(serializer=strip_and_join)
    categorias2 = scrapy.Field(serializer=strip_and_join)
    categorias3 = scrapy.Field(serializer=strip_and_join)
    qtdCategorias = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
    image_name = scrapy.Field()

#define pipeline

class MyImagesPipeline(ImagesPipeline):
    CONVERTED_ORIGINAL = re.compile('^full/[0-9,a-f]+.jpg$')
    def get_media_requests(self, item, info):
        return [Request(x, meta={'image_name': item['image_name']})
                for x in item.get('image_urls', [])
                ]
    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        print "get_images"
        for key, image, buf, in super(MyImagesPipeline, self).get_images(response, request, info):
            if self.CONVERTED_ORIGINAL.match(key):
                key = self.change_filename(key, response)
            yield key, image, buf

    def change_filename(self, key, response):
        return "full/%s.jpg" % str(response.meta['image_name'])

class CrawlerpaodeacucarPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('produtos.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class CSVWriterPipeline(object):
    pass

class MyProjectCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter
        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
            kwargs['fields_to_export'] = fields_to_export
        super(MyProjectCsvItemExporter, self).__init__(*args, **kwargs)



#define spider
class SpiderprodutosSpider(scrapy.Spider):
    name = "spiderProdutos"
    allowed_domains = ["paodeacucar.com.br"]
    start_urls = [
        'http://www.paodeacucar.com.br/',
   ]

    # Extrair links de todas as categoria dos produtos
    def parse(self, response):
        #extraindo todas a categorias da primeira div todos os produtos
        for href in response.xpath('//*[@id="nhgpa_submenu_1"]/div[@class="nhgpa_list nhgpa_first-submenu"]/a/@href'):
            url = response.urljoin(href.extract())
            self.logger.debug('Retrieved URL: %s', url)
            yield scrapy.Request(url, callback=self.navegarNaPaginaDaCategoria)
        # extraindo todas a categorias da segunda e terceira div todos os produtos
        for href in response.xpath('//*[@id="nhgpa_submenu_1"]/div[@class="nhgpa_list nhgpa_first-submenu"]/a/@href'):
            url = response.urljoin(href.extract())
            self.logger.debug('Retrieved URL: %s', url)
            yield scrapy.Request(url, callback=self.navegarNaPaginaDaCategoria)

    #Extrair lista de links de produtos dispostos em páginas de navegação
    def navegarNaPaginaDaCategoria(self, response):
        for href in response.xpath('//*[@id="showcase"]/div/div[1]/h3/a/@href'):
            url = response.urljoin(href.extract())
            self.logger.debug('Retrieved URL: %s', url)
            yield scrapy.Request(url, callback=self.parse_dir_contentsProdutos)

        result = response.xpath('//*[@id="paginator"]/div/nav/ul/li[1]/nav/ul/li[last()-1]/a/text()').extract()
        maxPage = 1
        if len(result) > 0:
            maxPage = int(result[0])-1 if result else 1;
            for page in range(1, maxPage):
                urlPaginas = response.urljoin("?&p="+str(page)+"&ftr=")
                yield scrapy.Request(urlPaginas, callback=self.extrairListaDeProdutos)

    def extrairListaDeProdutos(self, response):
        for href in response.xpath('//*[@id="showcase"]/div/div[1]/h3/a/@href'):
            url = response.urljoin(href.extract())
            self.logger.debug('Retrieved URL: %s', url)
            yield scrapy.Request(url, callback=self.parse_dir_contentsProdutos)


    def parse_dir_contentsProdutos(self, response):
        item = CrawlerpaodeacucarItem()
        item['nome'] = response.xpath('//*[@id="productArea"]/div[1]/header/h1/text()').extract()
        item['id'] = str(response.url).split("/")[4]
        item['preco'] = response.xpath('//*[@id="productForm"]/div[1]/span[2]/text()').extract()
        item['categorias1'] = response.xpath('//*[@id="breadCrumbArea"]/nav/ul/li[1]/a/text()').extract()
        item['categorias2'] = response.xpath('//*[@id="breadCrumbArea"]/nav/ul/li[2]/a/text()').extract()
        item['categorias3'] = response.xpath('//*[@id="breadCrumbArea"]/nav/ul/li[3]/a/text()').extract()
        item['qtdCategorias'] = len(response.xpath('//*[@id="breadCrumbArea"]/nav/ul/li/a/text()').extract())
        link = response.xpath('//*[@id="product-image"]/a/@href').extract()
        if("#" in link):
            link = response.css('#product-image > a.zoomImage.product-image__zoom-trigger > img').xpath('@src').extract()
        item['image_urls'] = ["http://www.paodeacucar.com.br"+str(link[0])]
        item['image_name'] = str(response.url).split("/")[4]
        #item['image'] = response.xpath('//*[@id="product-image"]/a/@href').extract()
        yield item


# callback fired when the spider is closed
def callback(spider, reason):
    stats = spider.crawler.stats.get_stats()  # collect/log stats?

    # stop the reactor
    reactor.stop()


# instantiate settings and provide a custom configuration
img_dir = os.path.join(os.getcwd(), 'images')
settings = Settings()
settings.set('ITEM_PIPELINES', {
    '__main__.MyImagesPipeline': 1,
    '__main__.JsonWriterPipeline': 800,
    '__main__.CSVWriterPipeline': 900,
})
settings.set('FEED_EXPORTERS', {
    'csv': '__main__.pipelines.MyProjectCsvItemExporter',
})
settings.set('FIELDS_TO_EXPORT', {
    'id','nome','preco', 'categorias1','categorias2','categorias3','image_name'
})
settings.set('CSV_DELIMITER', ';')
settings.set('IMAGES_STORE', img_dir)
settings.set('DOWNLOAD_HANDLERS', {'s3': None})




# instantiate a crawler passing in settings
crawler = Crawler(settings)

# instantiate a spider
spider = SpiderprodutosSpider()

# configure signals
crawler.signals.connect(callback, signal=signals.spider_closed)

# configure and start the crawler
crawler.configure()
crawler.crawl(spider)
crawler.start()

# start logging
log.start()

# start the reactor (blocks execution)
reactor.run()