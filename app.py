from flask import Flask, jsonify, request
# import search_tweets
# import sentiment_analysis
# import get_hashtag_for_search
# import scrape_google_reviews
# import count_tweets
import handlers
import pandas as pd
import get_google_search_company_details
from logging_python import logger

app = Flask(__name__)


def get_handles_from_company_name(company_lower_case):
    df = pd.read_csv("Company Reviews - handles.csv")
    company_lower_case = company_lower_case.lower()

    if company_lower_case in list(df["Company_lower_case"]):
        logger.info("Name exists in companies handles")
        print("Name in companies handles")
        row = df.loc[df["Company_lower_case"] == company_lower_case]
        playstore_query = row["Playstore"].values[0]
        # appstore_name, appstore_id = str(row["Appstore"].values[0]).split("/id")
        appstore_query = row["Appstore"].values[0]
        twitter_query = str(row["Twitter"].values[0])
        logo = str(row["logo_link"].values[0])
        logger.info(playstore_query + appstore_query + twitter_query + logo)

        print(playstore_query, appstore_query, twitter_query, logo)

    else:
        logger.info("Name not in companies handles")

        print("Name not in companies handles")

        playstore_query, appstore_query, twitter_query, logo = get_google_search_company_details.get_company_handles_from_query(
            company_lower_case)
        logger.info(playstore_query + appstore_query + twitter_query + logo)


    return playstore_query, appstore_query, twitter_query, logo


#
# def get_tweet_response(query):
#
#     tweet_fields = "tweet.fields=text,created_at&max_results=100&expansions=author_id&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
#
#     response = search_tweets.search_twitter(query, tweet_fields)
#     hashtags = get_hashtag_for_search.json_to_hashtags(query, response)
#     print("hashtags" , hashtags)
#     response = response["data"]
#     response, sentiment = sentiment_analysis.take_list_oftweets_give_actions(response, filter)
#     response.append({"sentiment" : sentiment})
#     response.append({ "hashtags" : hashtags})
#
#     print("="*80)
#     print("response  ::: " , response)
#     print(len(response))
#
#     return jsonify(response)

# def get_play_store_response(query):
#     response = scrape_google_reviews.scrape(query)
#     return response


@app.route('/tweet_count', methods=['GET'])
def tweet_count_fn():
    query = request.args["brand"]
    # query = "@monzo"

    print("query  :  " + query)
    tweet_fields = "granularity=day"

    response = count_tweets.search_counts(query)

    return jsonify(response)


@app.route('/test', methods=['GET'])
def test():
    logger.info("server working")

    return "server working"


@app.route('/', methods=['POST', 'GET'])
def hello():
    logger.info("=" * 80)
    query = request.args["brand"]

    playstore_query, appstore_query, twitter_query, logo = get_handles_from_company_name(query)
    # playstore_query, appstore_query, twitter_query, logo = get_google_search_company_details.get_company_handles_from_query(query)
    # sectors = request.args["sectors"]
    # filter = request.args["filter"]
    sectors = ["food", "riding", "tech", "delivery", "features"]
    logger.info("query  :  " + str(appstore_query))

    feedback_response, count_labels , graph_data, graph_options= handlers.handle_request(twitter_query, playstore_query, appstore_query, sectors)
    response = {"feedback": feedback_response,
                "logo": logo,
                "handles": str(playstore_query + "," + appstore_query + "," + twitter_query + "," + logo),
                "labels": count_labels,
                "graphData" : graph_data,
                "graphDataOptions" : graph_options}

    # logger.info(response)

    return jsonify(response)



@app.route('/get_org_info', methods=['POST', 'GET'])
def get_org_info():
    req = request.get_json()
    orgId = req["orgId"]
    logger.info("=" * 80)
    response = {
                "orgId": orgId,
                "name": "Roundpier",
                "logo": "logo",
                "topics" : ["topic1", "topic2"],
                }
    logger.info(response)
    return jsonify(response)

if __name__ == '__main__':
    # get_handles_from_company_name("uber eats")
    app.run(host="0.0.0.0", port=8000)
