import requests
import json
import credentials, get_hashtag_for_search
import pandas as pd
import csv


BEARER_TOKEN = credentials.TWITTER_BEARER_TOKEN

def form_better_dataframes(search_tweets):
    print("----------"*30)

    search_tweets_with_location = []


    for tweet in search_tweets["data"]:
        for user in search_tweets["includes"]["users"]:
            print(user)
            print(tweet)
        #     break
        # break
            if user["id"] == tweet["author_id"] and "location" in user:
                print(tweet, tweet["author_id"], user["id"], user["location"])
                tweet["location"] = user["location"]
                search_tweets_with_location.append(tweet)
    df = pd.DataFrame(search_tweets_with_location)
    return df



def save_file_to_local(query, search_result):
    # print(search_result.json()["meta"]["result_count"])

    if search_result.json()["meta"]["result_count"] == 0:
        return {"data" : [{"text" : "No results", "polarity" : ""}]}

    # # json.dumps(search_result, indent=4, sort_keys=True)
    # with open('Data/{}.json'.format(query), 'w') as fp:
    #     json.dump(search_result.json(), fp, indent=4)

    json_response_df = pd.DataFrame(search_result.json()["data"])
    json_response_df = form_better_dataframes(search_result.json())
    # json_response_df[["created_at", "text" , "id"]].to_csv("Data/{}.csv".format(query), mode="a", index=False)
    json_response_df[["text", "id", "location"]].to_csv("Data3/{}.csv".format(query), mode="a", index=False)
    CSV_FILE = "Data3/{}.csv".format(query)
    data_overall_df = pd.read_csv(CSV_FILE, index_col=None)
    print(data_overall_df)
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        a = list(reader)
    print (len(a))

    return {
        "data" : a
    }

    # return search_result.json()

def search_twitter(query, tweet_fields ):
    bearer_token = BEARER_TOKEN
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )
    # url = "https://api.twitter.com/2/tweets/counts/recent?query={}&{}".format(
    #     query, tweet_fields
    # )
    search_response = requests.request("GET", url, headers=headers)
    print("="*80)
    print(print(json.dumps(search_response.json(), indent=4, sort_keys=True)))

    # json_response_df = pd.DataFrame(search_response.json()["data"])
    # json_response_df.to_csv("Data/{}.csv".format(query), mode="a", index=False)
    #
    # data_overall_dict = pd.read_csv("Data/{}.csv".format(query)).T.to_dict()

    print(search_response.status_code)

    if search_response.status_code != 200:
        raise Exception(search_response.status_code, search_response.text)
    return save_file_to_local(query, search_response)
    # print(search_response.json())

    # return search_response.json()
    # return search_response["data"]

if __name__ == '__main__':

    query = "Boris Johnson"
    # query = "Credit Suisse"
    # query = "HSBC"
    # query = "UKraine"
    # query = "Nato"
    # query = "Boris Johnson"
    # query = "Narendra Modi"
    # query = "world war"
    # query = "russia"
    # tweet_fields = "tweet.fields=text,created_at,geo&place.fields=contained_within,country,country_code,full_name"
    # tweet_fields = "tweet.fields=text,created_at,geo&max_results=10&expansions=geo.place_id&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type"
    # tweet_fields = "tweet.fields=text,created_at,entities,geo&max_results=100&expansions=geo.place_id"
    tweet_fields = "tweet.fields=text,created_at,id&max_results=100&expansions=author_id&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
    # tweet_fields = "tweet.fields=text,created_at&max_results=100"
    # tweet_fields = "tweet.fields=text"

    json_response = search_twitter(query=query, tweet_fields=tweet_fields)
    # print(json.dumps(json_response, indent=4, sort_keys=True))

    # json_response_df = pd.DataFrame(json_response["data"])
    # with open(saveAddr + ".csv", 'a') as allpckts:
    # json_response_df.to_csv("Data/{}.csv".format(query), mode="a")
    # print(json_response_df)

    get_hashtag_for_search.json_to_hashtags(query, json_response)



