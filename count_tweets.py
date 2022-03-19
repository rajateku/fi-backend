import requests
import json
import credentials
import pandas as pd
# import matplotlib.pyplot as plt

BEARER_TOKEN = credentials.TWITTER_BEARER_TOKEN


def get_plot(data):
    dates = []
    PM_25 = []

    for a in data["data"]:
        dates.append(a["end"])
        PM_25.append(a["tweet_count"])

    dates = [pd.to_datetime(d) for d in dates]

    # plt.plot_date(dates, PM_25, fmt='-o')
    # plt.savefig("counts.png")

    # print(data["data"])
    return data["data"]

    # plt.scatter(dates, PM_25, s=100, c='red')

def search_counts(query):
    print("inside search counts")
    tweet_fields = "granularity=day"

    headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}


    url = "https://api.twitter.com/2/tweets/counts/recent?query={}&{}".format(
        query, tweet_fields
    )
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    plot_data = response.json()["data"]
    print( plot_data)
    return plot_data

if __name__ == '__main__':
    query = "@monzo"
    # tweet_fields = "tweet.fields=text,created_at,geo&place.fields=contained_within,country,country_code,full_name"
    # tweet_fields = "tweet.fields=text,created_at,geo&max_results=10&expansions=geo.place_id&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type"
    # tweet_fields = "tweet.fields=text,created_at,geo&max_results=100&expansions=geo.place_id&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type"
    tweet_fields = "granularity=day"
    search_counts(query)

    # json_response = search_twitter(query=query, tweet_fields=tweet_fields, bearer_token=BEARER_TOKEN)
    # print(json.dumps(json_response, indent=4, sort_keys=True))