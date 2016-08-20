# -*- coding: utf-8 -*-
import scrapy
from ..items import CrawlerpaodeacucarItem
from scrapy.utils.misc import load_object
import logging
from scrapy.utils.log import configure_logging
import Tkinter


configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)

class SpiderprodutosSpider(scrapy.Spider):
    name = "spiderProdutos"
    allowed_domains = ['paodeacucar.com.br']
    start_urls = [
        'http://www.paodeacucar.com.br/'
    ]
    # Extrair links de todas as categoria dos produtos
    def parse(self, response):
        #extraindo todas a categorias da primeira div todos os produtos
        for href in response.xpath('//*[@id="nhgpa_submenu_1"]/div[@class="nhgpa_list nhgpa_first-submenu"]/a/@href'):
            url = response.urljoin(href.extract())
            print(self.logger.debug('Retrieved URL: %s', url))
            yield scrapy.Request(url, callback=self.navegarNaPaginaDaCategoria)
        # extraindo todas a categorias da segunda e terceira div todos os produtos
        for href in response.xpath('//*[@id="nhgpa_submenu_1"]/div[@class="nhgpa_list nhgpa_first-submenu"]/a/@href'):
            url = response.urljoin(href.extract())
            print(self.logger.debug('Retrieved URL: %s', url))
            yield scrapy.Request(url, callback=self.navegarNaPaginaDaCategoria)
    #Extrair lista de links de produtos dispostos em páginas de navegação
    def navegarNaPaginaDaCategoria(self, response):
        for href in response.xpath('//*[@id="showcase"]/div/div[1]/h3/a/@href'):
            url = response.urljoin(href.extract())
            print(self.logger.debug('Retrieved URL: %s', url))
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
            print(self.logger.debug('Retrieved URL: %s', url))
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

