# -*- coding: utf-8 -*-
import scrapy

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


