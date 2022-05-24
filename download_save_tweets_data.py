import requests
import json
import credentials, get_hashtag_for_search
import pandas as pd
import csv
import os
import read_write_db


from logging_python import logger

BEARER_TOKEN = credentials.TWITTER_BEARER_TOKEN

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

    df1 = form_better_dataframes(search_result.json())
    CSV_FILE = CSV_FOLDER + "{}.csv".format(query)
    print(df1)
    # df_all = pd.read_csv(CSV_FILE)

    # df_all = pd.concat([df1, df_all]).drop_duplicates(ignore_index=True)
    # df_final = df_all.drop_duplicates(subset=['id'])
    df1[[TEXT, ID, LOCATION, CREATED_AT]].to_csv(CSV_FILE, mode="w", index=False)

    # data_overall_df = pd.read_csv(CSV_FILE, index_col=None)
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        a = list(reader)

    return {
        "data": a
    }


def search_and_save_twitter(query, table_name):
    bearer_token = BEARER_TOKEN
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, TWEET_FIELDS
    )

    search_response = requests.request("GET", url, headers=headers)
    logger.info(search_response.status_code)
    print(search_response.status_code)

    if search_response.status_code != 200:
        raise Exception(search_response.status_code, search_response.text)

    for tweet in search_response.json()["data"]:
        print(tweet)
        review = {}
        review["title"] = tweet[TEXT]
        review["content"] = tweet[TEXT]
        review["created_at"] = tweet[CREATED_AT]
        review["rating"] = ""
        review["id"] = tweet[ID]
        read_write_db.create_review(TableName=table_name, item=review)
        # break

    # response = save_file_to_local(query, search_response)
    return tweet


if __name__ == '__main__':
    query = "@Deliveroo"
    json_response = search_and_save_twitter(query=query)
    # get_hashtag_for_search.json_to_hashtags(query, json_response)
