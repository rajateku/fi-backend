import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os

from google_play_scraper import app, Sort, reviews_all
import json
import pandas as pd
import numpy as np


# print(k)

# playstore_handle = "com.nicheinc.nichealpha"
# playstore_handle = "com.deliveroo.orderapp"
# playstore_handle = "org.goodwall.app"
# playstore_handle = "com.udemy.android"
playstore_handle = "com.bumble.app"
# playstore_handle = "com.zeemee.zeemee_android"
# playstore_handle = "com.plexussmobiles"
# 'com.roundpier.roundpier'

result = app(
    playstore_handle,
    lang='en', # defaults to 'en'
    country='us' # defaults to 'us'
)
# print(result["comments"])

# for comment in result["comments"]:
    # print("="*30)
    # print(comment)

# print(len(result["comments"]))

def form_scrape_response(reviews):
    response = []
    i = 0
    for review in reviews:
        i+=1
        r = {"text" : review["content"],  "id" : i, "html" : "Pos" , "polarity" : "" , "location" : "" }
        response.append(r)
    return response

def scrape(query):
    print("Scraping google reviews")
    uk_reviews = reviews_all(
        query,
        sleep_milliseconds=0, # defaults to 0
        lang='en', # defaults to 'en'
        country='uk', # defaults to 'us'
        sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
        count=30
    )
    print(len(uk_reviews))
    print(uk_reviews)

    df_busu = pd.DataFrame(np.array(uk_reviews),columns=['review'])
    df_busu = df_busu.join(pd.DataFrame(df_busu.pop('review').tolist()))
    if os.path.exists("Data3/{}.csv".format(query)):
        pass
    else:
        df_busu.to_csv("Data3/{}.csv".format(query), mode="a", index=False)
    # print(df_busu.head())
    response = form_scrape_response(uk_reviews)
    print(response)


    return response

if __name__ == '__main__':
    scrape("com.roundpier.roundpier")
    # scrape('org.goodwall.app')