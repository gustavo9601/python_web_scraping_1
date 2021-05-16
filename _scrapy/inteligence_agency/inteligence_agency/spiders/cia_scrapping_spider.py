import scrapy


# Xpath

# Links
# Verifica todos los a, que su atributo href empiece por el parametro, y que su padre puede ser cualquier
# de los pasados, y se obtiene el atributo href
# //a[starts-with(@href, "/readingroom/collection") and (parent::h3|parent::h2|parent::p)]/@href

# h1 con clase documentFirstHeading obtengo el texto
# //h1[@class="documentFirstHeading"]/text()

# Todos los divs con clase field-item even, en su interior p que no tengan clase, y obtenga el texto
# //div[@class="field-item even"]//p[not(@class)]/text()

# Todos los div con clase field-item even, dentro todos los a, que no tengan clase y que target sea_blank, extrae el src de la img
# //div[@class="field-item even"]//a[not(@class) and @target="_blank"]/img/@src

class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = [
        'https://www.cia.gov/readingroom/'
    ]
    custom_settings = {
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_declassified = response.xpath(
            '//a[starts-with(@href, "/readingroom/collection") and (parent::h3|parent::h2|parent::p)]/@href').getall()
        # remove duplicates registers
        links_declassified = list(set(links_declassified))

        for link in links_declassified:
            print("*********************************")
            print("link to search", response.urljoin(link))
            print("*********************************")
            # Uniendo el path completo, con la parte del link
            # response.urljoin(link)
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):

        link = kwargs['url']
        title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
        img = response.xpath('//div[@class="field-item even"]//a[not(@class)]/img/@src').get()
        paragraphs = self.merge_paragraphs(
            response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').getall())

        yield {
            'url': link,
            'title': title,
            'img': img,
            'paragraphs': paragraphs
        }

    def merge_paragraphs(self, paragraphs):
        merge_paragraphs = ''
        for paragraph in paragraphs:
            merge_paragraphs += paragraph
        return merge_paragraphs

# %%
# Ejecutando el crawler por consola
# scrapy crawl cia
