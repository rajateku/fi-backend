### Trustpilot data scraping module

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import math
import time
import requests
import lxml.html as html
from bs4 import BeautifulSoup
import read_write_db


def scrape(query, table_name):
    if str(query) == "-" or   str(query) == "nan":
        print("No trustpilot")
        return "No trustpilot"

    reviewPage = query
    resultsPerPage = 20
    page = requests.get(reviewPage, verify=False)
    tree = html.fromstring(page.content)
    print("tree_path")

    ratingCount = tree.xpath('//span[@class="typography_typography__QgicV typography_h2__wAVpO typography_weight-medium__UNMDK typography_fontstyle-normal__kHyN3 styles_reviewCount__wGBxK"]')
    ratingCount = int(ratingCount[0].text.replace(',',''))

    tot_chunks = 20

    throttle = True
    sleepTime = 1

    # Total pages to scrape
    pages = math.ceil(ratingCount / resultsPerPage)
    print('Found total of ' + str(pages) + ' pages to scrape')


    print('Processing..')
    all_reviews = []
    for i in range(1, pages + 1):
        try:
            if (throttle): time.sleep(1)
            page = requests.get(reviewPage + '?page=' + str(i))
            tree = html.fromstring(page.content)
            script_bodies = tree.xpath(
                '//section[@class="styles_reviewContentwrapper__zH_9M"]' )

            soup = BeautifulSoup(page.content, "html.parser")
            for tag in soup.find_all("article"):
                review = {"content" : "",
                          "created_at" : "",
                          "rating"  : ""}
                print("===========")

                overallcontent = tag.find('div', {'class': 'styles_reviewContent__0Q2Tg'})
                content = overallcontent.find('p').get_text(separator="\n")
                title = overallcontent.find('h2').get_text()
                rating = tag.find('div', {'class': 'star-rating_starRating__4rrcf star-rating_medium__iN6Ty'}).find("img").get("alt")
                ts = tag.find('time').get("datetime")

                print(title)
                print(content)
                print(rating)
                print(ts)

                review["title"] = title
                review["content"] = content
                review["created_at"] =ts
                review["rating"] = rating
                read_write_db.create_review(TableName= table_name , item = review)
        except:
            pass
        break
    print('Processed ' + str(ratingCount) + '/' + str(ratingCount) + ' ratings.. Finished!')


if __name__ == '__main__':
    TableName = 'trustpilot_deliveroo2'
    read_write_db.create_table(TableName=TableName, key="created_at")
    query = 'http://www.trustpilot.com/review/www.deliveroo.co.uk'
    scrape(query=query, table_name=TableName)

