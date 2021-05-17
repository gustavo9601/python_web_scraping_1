import bs4
import requests
from common import config


class NewsPage:
    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._url = url
        self._visit(url)

    def _select(self, query_string):
        return self._html.select(query_string)

    def _visit(self, url):
        response = requests.get(url)

        # If something fail
        response.raise_for_status()

        self._html = bs4.BeautifulSoup(response.text, 'html.parser')



class HomePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)


    # @property // Similitud a un gettter de un atributo de clase
    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_articles_links']):
            # Verify if link exists and has the attr href
            if link and link.has_attr('href'):
                link_list.append(link)

        # List comprenhension with filter if contains string
        return list(set(link['href'] for link in link_list if self._url in link['href']))

class ArticlePage(NewsPage):

    def __init__(self, news_site_uid, url):
        super().__init__(news_site_uid, url)

    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        print("****result******")
        return result[0].text if len(result) else ''


    @property
    def title(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''