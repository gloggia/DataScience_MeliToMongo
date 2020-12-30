import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup



class Artículo(Item):
    título = Field()
    precio = Field()
    #descripción = Field()
    rooms = Field()
    baths = Field()

class MercadoLibreCrawler(CrawlSpider):
    name = 'melispider'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 3

    }
    download_delay = 1
    #=70620*1.645*1.645*0.5*0.5/(0.05*0.05*(70620-1)+ 1.645*1.645*0.5*0.5) = 270 casos
    allowed_domains = ['departamento.mercadolibre.com.ar', 'inmuebles.mercadolibre.com.ar/departamentos']   #puedo poner más dominios solo poniendo comas


    start_urls = ['https://inmuebles.mercadolibre.com.ar/departamentos/propiedades-individuales//capital-federal/']


    rules = (
        Rule(  # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/_Desde_\d+'
            ), follow=True),

        Rule(   # REGLA #2 => VERTICALIDAD AL DETALLE PRODUCTOS
            LinkExtractor(
                allow=r'/MLA-'
            ), follow=True, callback='parse_items'),
    )

    def limpiarTexto(self,texto):
        nuevoTexto= texto.replace('\n',' ').replace('\r',' ').replace('\t',' ').strip()
        return nuevoTexto


    def parse_items(self, response):
        item = ItemLoader(Artículo(), response)

        item.add_xpath('título', '//h1/text()', MapCompose(self.limpiarTexto))
        #item.add_xpath('descripción', '//div[@class="item-description__text"]/p/text()', MapCompose(self.limpiarTexto))
        item.add_xpath('precio', '//span[@class="price-tag-fraction"]/text()')
        item.add_xpath('rooms', '//dd[@class="align-room"]/text()',MapCompose(self.limpiarTexto))
        item.add_xpath('baths', '//dd[@class="align-bathroom"]/text()',MapCompose(self.limpiarTexto))
        yield item.load_item()

#scrapy runspider MercadoLibreEC.py -o mercado_librec.csv -t csv
