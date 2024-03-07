# This module developed specifically for interaction with web UI of Tech Church
# and able to transfer fetched response as Json or HTML structure into another modules

import requests
import json
import texttable
from bs4 import BeautifulSoup

AUTHOR_PUBLICATIONS_ENDPOINT = ('https://techcrunch.com/wp-json/tc/v1/magazine?_embed=true'
                                '&_envelope=true&author_name={author_name}'
                                '&include_developing_stories=true&page=2&cachePrevention=0')
# 'https://techcrunch.com/author/{author_name}/'

SEARCH_ENDPOINT = ('https://search.techcrunch.com/search;_ylc='
                   'X3IDMgRncHJpZAMzc0lIQ0VKWVNGdUdYYTBmUGY1cFRBBG5fc3VnZwM4BHBvcwMwBHBxc3RyAwRw'
                   'cXN0cmwDMARxc3RybAM0BHF1ZXJ5A3Rlc3QEdF9zdG1wAzE3MDk3MTYxNDI-?p={term}&fr=techcrunch')

TECHS_ENDPOINT = ('https://techcrunch.com/wp-json/tc/v1/magazine?page={page_number}&'
                  '_embed=true&_envelope=true&categories={category_num}&cachePrevention=0')

categories = {'apps': 577051039, 'startups': 20429, 'venture': 577030455, 'security': 21587494, 'ai': 577047203, 'cryptocurrency': 576601119, 'fintech': 577030453}


EVENTS_ENDPOINTS = ('https://techcrunch.com/wp-json/wp/v2/tc_events?_embed=true&upcoming=true&parent=0&cachePrevention=0',
          'https://techcrunch.com/wp-json/wp/v2/tc_events?_embed=true&past=true&parent=0&cachePrevention=0',
          'https://techcrunch.com/wp-json/wp/v2/tc_event?hide_empty=false&per_page=99&parent=0&cachePrevention=0',
          'https://techcrunch.com/wp-json/wp/v2/tc_events?_embed=true&featured=event_home&parent=0&cachePrevention=0')


def fetch_url(url):  # Just fetch a certain URL and returns the response text
    resp = requests.get(url)
    return resp.text


def get_publications_using_search(search_term):
    url = SEARCH_ENDPOINT.format(term=search_term)


def get_certain_author_publications(author_name):  # Will return response as a json object
    url = AUTHOR_PUBLICATIONS_ENDPOINT.format(author_name=author_name)
    return json.loads(fetch_url(url))


def get_certain_subject_publications(subject_code, pg_num):  # Will return response as a json object
    url = TECHS_ENDPOINT.format(category_num=subject_code, page_number=pg_num)
    return json.loads(fetch_url(url))


def get_publication_tags(soup):
    print(soup)
