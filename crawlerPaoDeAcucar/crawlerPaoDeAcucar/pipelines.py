# -*- coding: utf-8 -*-
import re
import json
from scrapy.http import Request
from scrapy.conf import settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import CsvItemExporter

class MyImagesPipeline(ImagesPipeline):
    CONVERTED_ORIGINAL = re.compile('^full/[0-9,a-f]+.jpg$')
    def get_media_requests(self, item, info):
        return [Request(x, meta={'image_name': item['image_name']})
                for x in item.get('image_urls', [])
                ]
    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        print "#### Extraindo Dados"
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