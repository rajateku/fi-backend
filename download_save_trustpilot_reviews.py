### Trustpilot data scraping module

## Imports
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import math
import csv
import time
import datetime
import json
import requests
import lxml.html as html
from bs4 import BeautifulSoup




## Configurations

# Trustpilot review page
basePage = 'http://www.trustpilot.com/review/'
reviewSite = 'www.deliveroo.co.uk'
reviewPage = basePage + reviewSite

# Data file to save to
datafile = 'dataSkype{}.csv'.format("_trustpilot")

# Trustpilot default
resultsPerPage = 20

print('Scraper set for ' + reviewPage + ' - saving result to ' + datafile)

## Count amount of pages to scrape

# Get page, skipping HTTPS as it gives certificate errors
page = requests.get(reviewPage, verify=False)
tree = html.fromstring(page.content)
print("tree_path")
# print(tree.xpath('typography_typography__QgicV typography_h2__wAVpO typography_weight-heavy__E1LTj typography_fontstyle-normal__kHyN3 styles_headline__HoyVg'))

# Total amount of ratings
ratingCount = tree.xpath('//span[@class="typography_typography__QgicV typography_h2__wAVpO typography_weight-medium__UNMDK typography_fontstyle-normal__kHyN3 styles_reviewCount__wGBxK"]')
# print(ratingCount)
ratingCount = int(ratingCount[0].text.replace(',',''))

# Amount of chunks to consider for displaying processing output
# For ex. 10 means output progress for every 10th of the data
tot_chunks = 20

# Throttling to avoid spamming page with requests
# With sleepTime seconds between every page request
throttle = True
sleepTime = 1

# Total pages to scrape
pages = math.ceil(ratingCount / resultsPerPage)
print('Found total of ' + str(pages) + ' pages to scrape')

## Main scraping section

with open(datafile, 'w', newline='', encoding='utf8') as csvfile:
    # Tab delimited to allow for special characters
    datawriter = csv.writer(csvfile, delimiter='\t')
    print('Processing..')
    all_reviews = []
    for i in range(1, pages + 1):

        # Sleep if throttle enabled
        if (throttle): time.sleep(1)

        page = requests.get(reviewPage + '?page=' + str(i))
        tree = html.fromstring(page.content)

        # Each item below scrapes a pages review titles, bodies and ratings

        script_bodies = tree.xpath(
            # '//p[@class="typography_typography__QgicV typography_body__9UBeQ typography_color-black__5LYEn typography_weight-regular__TWEnf typography_fontstyle-normal__kHyN3"]')
            # '//article[@class="paper_paper__1PY90 paper_square__lJX8a card_card__lQWDv styles_reviewCard__hcAvl"]' )
            '//section[@class="styles_reviewContentwrapper__zH_9M"]' )

        soup = BeautifulSoup(page.content, "html.parser")
        for tag in soup.find_all("article"):
            review = {"content" : "",
                      "created_at" : "",
                      "rating"  : ""}
            print("===========")
            # print(tag.find("div"))
            # print(tag.find('p').get_text())
            overallcontent = tag.find('div', {'class': 'styles_reviewContent__0Q2Tg'})
            content = overallcontent.find('p').get_text()
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
            all_reviews.append(review)
        break
    json_object = json.dumps(all_reviews, indent=4)
    print(json_object)
    dt = datetime.datetime.now()
    with open("data_jsons/{}_{}.json".format(reviewSite, datetime.datetime.now()), "w") as outfile:
        json.dump(all_reviews, outfile)


            # print(tag.get_text(separator=" "))
            # break
        # break

        # for idx, elem in enumerate(script_bodies):
        #
        #     # print(idx, elem.text_content())
        #     # print(idx, elem.items())
        #     print(elem.xpath('//p[contains(@class, "typography_typography__QgicV")]//a')[0].text_content())
        #     print(elem.xpath('//p').text_content())
        #
        #
        #     print(elem.xpath('//time/@datetime')[0])
        #     # print(elem.xpath('//p')[1].text_content())
        #     # print(elem)
        #     # curr_item = json.loads(elem.text_content())
        #     #
        #     # # Progress counting, outputs for every processed chunk
        #     # reviewNumber = idx + 20 * (i - 1) + 1
        #     # chunk = int(ratingCount / tot_chunks)
        #     # if (reviewNumber % chunk == 0):
        #     #     print('Processed ' + str(reviewNumber) + '/' + str(ratingCount) + ' ratings')
        #     #
        #     # title = curr_item["reviewHeader"]
        #     # body = curr_item["reviewBody"]
        #     # rating = curr_item["stars"]
        #     # print([title, body, rating])
        #     #
        #     # datawriter.writerow([title, body, rating])
        # break

    print('Processed ' + str(ratingCount) + '/' + str(ratingCount) + ' ratings.. Finished!')