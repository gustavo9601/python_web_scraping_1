# Libreria para recibir parametros por consola
import argparse
# Libreria para mejorar los print por consola
import logging
# Import config in file config.yaml
from common import config
# Import news object
import news_page_objects as news
# Errors exepctions
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

import datetime
import pandas as pd

# Configuracion inicial del loggin
logging.basicConfig(level=logging.INFO)
# Especificando al logger en donde se esta ejecutando __name__ => filename.py
logger = logging.getLogger(__name__)


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']

    logging.info(f'Begining scraper for: {host}')
    hompage = news.HomePage(news_site_uid, host)
    articles = []
    for link in hompage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article:
            article_structure = {
                'title': article.title,
                'body': article.body,
                'link': link,
                'host': host
            }
            articles.append(article_structure)
            logger.info(f'OK Article: [{link}] for the host [{host}]')

    print(f"Articles founded {len(articles)}")
    _save_articles(news_site_uid, articles)


def _save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime('%Y_%m_%d')

    out_file_name = f"./../outputs/{now}_{news_site_uid}_articles.csv"
    print(out_file_name)
    df = pd.DataFrame(articles)
    df.to_csv(out_file_name, index=False)


def _fetch_article(news_site_uid, host, link):
    logger.info(f'Start fetching article in the url: [{link}] for the host [{host}]')
    article = None
    try:
        article = news.ArticlePage(news_site_uid, link)
    except (HTTPError, MaxRetryError) as e:
        # exc_info=False // indica que no muestre el error por consola
        logger.warning(f'Error while fetching the article in the url: [{link}] for the host [{host}]', exc_info=False)

    # Si devuelve algo la respuesta, y no es nulo el body
    if article and not article.body:
        logger.warning(f'Not found article in the url: [{link}] for the host [{host}]')
        return None

    return article


if __name__ == '__main__':
    # py main.py --help
    parser = argparse.ArgumentParser()
    news_site_choices = list(config()['news_sites'].keys())

    # Añadiendo argumento news_site que se podra recibir por consola
    parser.add_argument('news_site',
                        help='The news site that you hat to scrape',
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)
