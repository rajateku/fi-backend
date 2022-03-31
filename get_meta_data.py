from google_play_scraper import app, Sort, reviews_all, reviews
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



def get_playstore_meta_data(query):
    # result = app(
    #     query,
    #     lang='en',  # defaults to 'en'
    #     country='us'  # defaults to 'us'
    # )
    # response = {}
    # response["title"] = result["title"]
    # response["histogram"] = result["histogram"]
    # response["installs"] = result["installs"]
    # response["score"] = result["score"]
    # response["ratings"] = result["ratings"]
    # response["reviews"] = result["reviews"]
    #
    # print(response)

    response = {'title': 'RoundPier: High School and College App', 'histogram': [11, 0, 5, 0, 22], 'installs': '1,000+', 'score': 3.5714285, 'ratings': 38, 'reviews': 5}

    return response


# get_playstore_meta_data("com.roundpier.roundpier")