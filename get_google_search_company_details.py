import requests
import urllib
from requests_html import HTMLSession
from urllib.parse import urlparse
from urllib.parse import parse_qs
from bs4 import BeautifulSoup
from logging_python import logger


def get_source(url):

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def scrape_google_play_store(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://play.google.com/store/apps/details')
    return_links = []

    for url in links[:]:
        if url.startswith(google_domains):
            return_links.append(url)
            # links.remove(url)

    return return_links

def scrape_app_store_app(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = 'https://apps.apple.com/'
    return_links = []

    for url in links[:]:
        if url.__contains__(google_domains):
            return_links.append(url)

    return return_links

def scrape_twitter(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = 'https://twitter.com/'
    return_links = []

    for url in links[:]:
        if url.__contains__(google_domains):
            return_links.append(url)

    return return_links




def get_google_img(query):
    """
    gets a link to the first google image search result
    :param query: search query string
    :result: url string to first result
    """
    url = "https://www.google.com/search?q=" + str(query)  + "&source=lnms&tbm=isch"
    headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    # print(url)
    html = requests.get(url, headers=headers).text

    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    image = soup.find("img",{"class":"yWs4tf"})
    # print(image)

    if not image:
        return
    return image['src']



def get_company_handles_from_query(company_searched):
    if len(company_searched.split())<3:
        google_search_query_playstore = "{} google play store apps".format(company_searched)
        google_search_query_appstore = "{} google app store apps".format(company_searched)
        google_search_query_logo = "{} company logo".format(company_searched)

    else:
        google_search_query_playstore = "{} google play store apps".format(company_searched)
        google_search_query_appstore = "{} google app store apps".format(company_searched)
        google_search_query_logo = "{} company logo".format(company_searched)


    play_store = scrape_google_play_store(google_search_query_playstore)
    app_store = scrape_app_store_app(google_search_query_appstore)
    logo = get_google_img(google_search_query_logo)

    # print(play_store[0])
    # print(app_store[0])
    parsed_url = urlparse(play_store[0])
    play_store_handle = parse_qs(parsed_url.query)['id'][0]
    app_store_handle = app_store[0].split("/app")[-1].replace("/id", "_").replace("/", "")
    # print("Handles :", play_store_handle, app_store_handle, "" , logo)

    return play_store_handle, app_store_handle, "", "-",  logo

if __name__ == '__main__':
    c_list = ["Deliveroo" ]
    for c in c_list:
        try:
            play_store_handle, app_store_handle, _ , logo= get_company_handles_from_query(c)
            print(play_store_handle, app_store_handle, "", logo)
        except:
            print("=== == ==")
            logger.error("can't get company name")
            pass

