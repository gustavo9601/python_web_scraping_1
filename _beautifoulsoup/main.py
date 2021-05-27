# Libreria para recibir parametros por consola
import argparse
# Libreria para mejorar los print por consola
import hashlib
import logging
# Import config in file config.yaml
from common import config
# Import news object
import news_page_objects as news
# Errors exepctions
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

# Tokenizacion de palabras
# Permite identificar las palabras de relevancia en un texto
import nltk
# lista de palabras sin significancia (el, la es, etc)
from nltk.corpus import stopwords

# Complementos necesarios de nltl
nltk.download('punkt')
nltk.download('stopwords')

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
    df = pd.DataFrame(articles)
    # Remove duplicates register by title
    df = _remove_duplicates_by_column(df, 'title')
    # Add column hash
    df = _add_column_hash_url(df)
    # Remove lines or baklslaes from the body
    df = _remove_lines_from_body(df)
    # Add column tokenize title
    df = _tokenizer_column(df, 'title')
    # Add column tokenize body
    df = _tokenizer_column(df, 'body')


    # Save to csv data
    df.to_csv(out_file_name)


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


def _tokenizer_column(df, column):
    # Definiendo a español el listado de palabras sin significancia
    stop_words = set(stopwords.words('spanish'))

    df['token_' + column] = (
        df.dropna()  # eliminando nan
            .apply(lambda row: nltk.word_tokenize(row[column]), axis=1)  # tokenizando el texto
            .apply(
            lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))  # filtrando solo valores alfanumericos
            .apply(
            lambda tokens: list(map(lambda token: token.lower(), tokens)))  # pipe para dejar en minuscula el texto
            .apply(lambda word_list: list(
            filter(lambda word: word not in stop_words, word_list)))  # filtrando solo palabras que sib significantes
            .apply(lambda valid_word_list: len(valid_word_list))  # devolviendo el conteo de valores de la lista
    )

    return df

def _remove_duplicates_by_column(df, column, keep='first'):
    # subset=[column]
    # Especifica el nombre de la columna por la cual se eliinara los duplicados

    # keep=keep
    # Especifica cual debe dejar, primero, ultimo
    df = df.drop_duplicates(subset=[column], keep=keep)
    return df

def _add_column_hash_url(df):
    logger.info('Generating uids from url hashed')
    # Hasheando link y despues se decodifica a heaxdecimal
    uids = (
        df.apply(lambda row: hashlib.md5(bytes(row['link'].encode())), axis=1)
            .apply(lambda has_object: has_object.hexdigest())
    )
    # Agregamos la nueva serie como columna del df
    df['uid'] = uids
    # Retornamos el nuevo df seteando la columna uid como indece
    return df.set_index('uid')


def _remove_lines_from_body(df):
    df['body'] = df.apply(lambda row: row['body'].replace('\n', ''), axis=1)
    return df


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
