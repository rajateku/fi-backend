import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import os
import csv

from google_play_scraper import app, Sort, reviews_all, reviews
import json
import pandas as pd
import numpy as np
from logging_python import logger


CSV_FOLDER = "Data4/"
if os.path.exists(CSV_FOLDER):
    pass
else:
    os.mkdir(CSV_FOLDER)


AUTHOR_ID = "author_id"
LOCATION = "location"
ID = "id"
TEXT = "text"
CREATED_AT = "created_at"
TWEET_FIELDS = "tweet.fields=text,created_at,id&max_results=10&expansions=author_id&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"


def form_better_dataframes(search_tweets):
    search_tweets_with_location = []

    for tweet in search_tweets["data"]:
        for user in search_tweets["includes"]["users"]:
            if user[ID] == tweet[AUTHOR_ID] and LOCATION in user:
                print(tweet, tweet[AUTHOR_ID], user[ID], user[LOCATION])
                tweet[LOCATION] = user[LOCATION]
                search_tweets_with_location.append(tweet)
    df = pd.DataFrame(search_tweets_with_location)
    return df


def save_file_to_local(query, search_result):
    if search_result.json()["meta"]["result_count"] == 0:
        return {"data": [{TEXT: "No results", "polarity": ""}]}

    json_response_df = form_better_dataframes(search_result.json())
    CSV_FILE = CSV_FOLDER + "{}.csv".format(query)
    print(json_response_df)
    json_response_df[[TEXT, ID, LOCATION, CREATED_AT]].to_csv(CSV_FILE, mode="a", index=False)

    data_overall_df = pd.read_csv(CSV_FILE, index_col=None)
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        a = list(reader)

    return {
        "data": a
    }
def get_title_of_app(competitor):
    result = app(
        competitor,
        lang='en',  # defaults to 'en'
        country='us'  # defaults to 'us'
    )
    title = result["title"]
    return title

def get_playstore_similar_apps(query):

    result = app(
        query,
        lang='en',  # defaults to 'en'
        country='us'  # defaults to 'us'
    )
    print(result["similarApps"])
    for competitor  in result["similarApps"]:
        title = get_title_of_app(competitor)
        print(title)

def scrape(query):
    print("Scraping google reviews")
    logger.info("Scraping google reviews")
    logger.info(query)
    uk_reviews = reviews(
        query,
        # sleep_milliseconds=0,  # defaults to 0
        lang='en',  # defaults to 'en'
        country='uk',  # defaults to 'us'
        sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
        count=500
    )
    print(len(uk_reviews))
    CSV_FILE = "Data4/{}.csv".format(query)

    df_busu = pd.DataFrame(np.array(uk_reviews[0]), columns=['review'])
    df_busu = df_busu.join(pd.DataFrame(df_busu.pop('review').tolist()))
    try:

        df1 = pd.read_csv(CSV_FILE)
        print(df1)
        print(df_busu)
        df_all = pd.concat([df1, df_busu]).drop_duplicates(ignore_index=True)
        df_final = df_all.drop_duplicates(subset=['reviewId'])
        df_final.to_csv("Data4/{}.csv".format(query), mode="w", index=False)
        print("try")


    # past_df.append(df_busu).drop_duplicates().to_csv(CSV_FILE, mode="a").reset_index(drop=True)
    except:
        df_busu.to_csv("Data4/{}.csv".format(query), mode="w", index=False)
        print("except")




    return df_busu

if __name__ == '__main__':
    # playstore_handle = "com.roundpier.roundpier"
    playstore_handle = "com.honeypot"

    query = playstore_handle
    # json_response = scrape(query=query)
    get_playstore_similar_apps(query)
