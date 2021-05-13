# %%
# Verificando la version en la consola
# scrapy version

# http://quotes.toscrape.com/

# Inicializando proyecto de scrappy
# scrapy startproject example_sandbox

# %%
# improtando
import scrapy
from scrapy.crawler import CrawlerProcess


# %%
# Clase de spider de configuracion

class QuotesSpider(scrapy.Spider):
    # Nombre con el que scrapy se referira al proyecto (debe ser unico)
    name = 'quotes_scrapping'
    # URLS a crawlear
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    # Propierdades de configuracio
    # para este caso se especifica nombre y formato del archivo a exportar para no tener que pasar -o por consola
    # FEED_URI
    # FEED_FORMAT

    # Maximas de peticiones a la ves
    # CONCURRENT_REQUESTS

    # Limitar cantidad de Mem ram qe puede tomar el proceso
    # MEMUSAGE_LIMIT_MB

    # Email denotificacion si se llega a pasar el limite de memoria
    # MEMUSAGE_NOTIFY_MAIL

    # Especifica si respeta o no las directrices del robtos.txt
    # ROBOTSTXT_OBEY

    # Setea el nombre de agente con el que enviara el request
    # USER_AGENT

    # Setea el encoding del texto
    # FEED_EXPORT_ENCODING
    custom_settings = {
        'FEED_URI': 'files_export/data_export.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['ing.gustavo.marquez@gmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'GusElMasPro',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    # Logica de tratamiento sobre la respuesta http
    def parse(self, response):
        print(response.status, response.headers)

        # Making a file and send the text
        self.make_file_test(response.text)

        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        # [contains(@class, "tags-box")] // permite buscar concidencia no exactas sobre la clase del elemento
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        # De esta forma podremos recibir la variable top por consola
        # de existir la variable top la asgina, en caso contrario retorna None
        # getattr(object, attribute_to_get, default_value_not_found)
        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            # Cortando la lista de haber enviado el parametro top
            top_tags = top_tags[:top]

        # Convirtiendo en generador la funcion parse
        yield {
            'title': title,
            'quotes': quotes,
            'top_tags': top_tags
        }

        # Extrayendo el path del boton
        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        # Verifica si retorna o encuentra el boton
        if next_page_button_link:
            # response.follow(new_path_to_go, callback=fucntion_to_execute_after_request)
            # Si se pasa esta misma funcion parse, se vuelve recursiva la funcion
            # Se puede pasar la logica a otra funcion, y si esta recibe valores se envian en el param cb_kwargs={}
            yield response.follow(next_page_button_link, callback=self.parse)

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            # .extend // push sobre el array quotes
            quotes.extend(response.xpath(
                '//span[@class="text" and @itemprop="text"]/text()').getall())

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]//li[@class="next"]/a/@href').get()

        # Si existe el boton con el link, recursivamente ira pusehando sobre el array quotes la data
        # hasta que no encuentre mingun link y retorne todo lo pusheado con el yield
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes})
        else:
            yield {
                'quotes': quotes
            }

    def make_file_test(self, text):
        with open('files_export/resultados.html', 'w', encoding='utf-8') as file:
            print('scrapy initial')
            # Escribiendo la respuesta html dentro de este nuevo fich
            file.write(text)

# %%
# Ejecutando el crawler por consola
# scrapy crawl quotes_scrapping

# Si la funcion parse, es un generador podemos pasar el parametro -o (output) para exportar directamente a un fich
# .json | .csv // etc
# scrapy crawl quotes_scrapping -o file_Export.json

# Pasando argumentos a la funcion
# top // nombre del parametro que recibiria el callback
# scrapy crawl quotes_scrapping -a top=2

# %%
# Abriendo una consola de scrappy para escribir directamente xpath sobre la url por parametro
# scrapy shell "http://quotes.toscrape.com/page/1"

# Sobre el objeto response, se puede ejecutar directamente xpath
# response.xpath('//h1/a/text()')

# .get()  // permite traer en raw la data
# response.xpath('//h1/a/text()').get()

# .getall() // permite traer varios elementos
# response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
