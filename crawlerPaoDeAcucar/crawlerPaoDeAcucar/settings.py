# -*- coding: utf-8 -*-
import os
img_dir = os.path.join(os.getcwd(), 'images')
BOT_NAME = 'crawlerPaoDeAcucar'

SPIDER_MODULES = ['crawlerPaoDeAcucar.spiders']
NEWSPIDER_MODULE = 'crawlerPaoDeAcucar.spiders'
DOWNLOAD_HANDLERS = { #'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
    'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    #'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    's3': None
}


#ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
ITEM_PIPELINES = { 'crawlerPaoDeAcucar.pipelines.MyImagesPipeline' : 1,
                   'crawlerPaoDeAcucar.pipelines.JsonWriterPipeline': 800,
                   'crawlerPaoDeAcucar.pipelines.CSVWriterPipeline': 900,
                   }

#IMAGES_STORE = 'C:/Users/Kevin/PycharmProjects/crawlerPaoDeAcucar/crawlerPaoDeAcucar/crawlerPaoDeAcucar/images'
IMAGES_STORE = img_dir
CSV_DELIMITER = ";"
FEED_EXPORTERS = {
    'csv': 'crawlerPaoDeAcucar.pipelines.MyProjectCsvItemExporter',
}

FIELDS_TO_EXPORT = [
    'id',
    'nome',
    'preco',
    'categorias1',
	'categorias2',
	'categorias3',
	'image_name'
]