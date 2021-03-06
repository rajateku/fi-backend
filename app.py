from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

# import search_tweets
# import sentiment_analysis
# import get_hashtag_for_search
# import scrape_google_reviews
# import count_tweets
import handlers
import handlers2
import bugs_detected_recommendations
from get_meta_data import get_playstore_meta_data
import pandas as pd
import json
import get_google_search_company_details
import read_write_db
import watchlist

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




def get_handles_from_company_name(company_lower_case):
    df = pd.read_csv("Company Reviews - handles.csv")
    company_lower_case = company_lower_case.lower()

    if company_lower_case in list(df["Company_lower_case"]):
        print("Name in companies handles")
        row = df.loc[df["Company_lower_case"] == company_lower_case]
        playstore_query = row["Playstore"].values[0]
        # appstore_name, appstore_id = str(row["Appstore"].values[0]).split("/id")
        appstore_query = row["Appstore"].values[0]
        twitter_query = str(row["Twitter"].values[0])
        trustpilot_query = str(row["Trustpilot"].values[0])
        logo = str(row["logo_link"].values[0])
        print(playstore_query + appstore_query + twitter_query + logo)

        print(playstore_query, appstore_query, twitter_query,trustpilot_query, logo)
        return {
            'twitter': twitter_query,
            'trustpilot': trustpilot_query,
            'appstore': appstore_query,
            'company_name': company_lower_case,
            'playstore': playstore_query,
            'logo' :logo
        }

    else:
        print("Name not in companies handles")

        print("Name not in companies handles")

        playstore_query, appstore_query, twitter_query,trustpilot_query, logo = get_google_search_company_details.get_company_handles_from_query(
            company_lower_case)
        print(playstore_query + appstore_query + twitter_query + trustpilot_query +logo)


    return playstore_query, appstore_query, twitter_query, trustpilot_query,  logo


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


@app.route('/', methods=['GET'])
@cross_origin()
def test():

    print("server working")

    return "server working with git push"


@app.route('/all', methods=['POST', 'GET'])
@cross_origin()
def hello():
    print("=" * 80)
    query = request.args["brand"]
    orgId = request.get_json()
    print(orgId)

    playstore_query, appstore_query, twitter_query,trustpilot_query, logo = get_handles_from_company_name(query)
    # playstore_query, appstore_query, twitter_query, logo = get_google_search_company_details.get_company_handles_from_query(query)
    # sectors = request.args["sectors"]
    # filter = request.args["filter"]
    sectors = ["food", "riding", "tech", "delivery", "features"]
    print("query  :  " + str(appstore_query))

    feedback_response, count_labels , graph_data, graph_options= handlers.handle_request(twitter_query, playstore_query, appstore_query,trustpilot_query, sectors)
    response = {"feedback": feedback_response,
                "logo": logo,
                "handles": str(playstore_query + "," + appstore_query + "," + twitter_query + "," + logo),
                "labels": count_labels,
                "graphData" : graph_data,
                "graphDataOptions" : graph_options}

    return jsonify(response)


@app.route('/all2', methods=['POST', 'GET'])
@cross_origin()
def all2():
    print("=" * 80)
    query = request.args["brand"].lower()

    # jwt = request.headers.get('jwt')
    # jwt_creds = jwt_auth.read_active_jwts(jwt)
    # print(jwt_creds["username"])
    # query = (jwt_creds["username"])

    # company_names_response = read_write_db.get_company_handles(TableName="company_handles", company_name = query )
    company_names_response = get_handles_from_company_name(query)
    print("company_names_response" , company_names_response)
    if company_names_response == None:
        response = {"feedback": [],
                    "labels": [],
                    "graphData": [],
                    "graphDataOptions": []}
    else:
        feedback_response , labels_sources, graph_data, graph_options = handlers2.get_dashboard_data(query)
        response = {"feedback": feedback_response,
                    "labels": labels_sources,
                    "graphData": graph_data,
                    "graphDataOptions": graph_options,
                    }

    return jsonify(response)

@app.route('/dashboard', methods=['POST', 'GET'])
@cross_origin()
def dashboard():
    print("=" * 80)
    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds)
    print(jwt_creds["username"])
    query = (jwt_creds["username"])

    # company_names_response = read_write_db.get_company_handles(TableName="company_handles", company_name = query )
    company_names_response = get_handles_from_company_name(query)
    print("company_names_response" , company_names_response)
    if company_names_response == None:
        response = {"feedback": [],
                    "labels": [],
                    "graphData": [],
                    "graphDataOptions": []}
    else:
        feedback_response , labels_sources, graph_data, graph_options = handlers2.get_dashboard_data(query)
        response = {"feedback": feedback_response,
                    "labels": labels_sources,
                    "graphData": graph_data,
                    "graphDataOptions": graph_options,
                    }

    return jsonify(response)



@app.route('/get_org_info', methods=['POST', 'GET'])
@cross_origin()
def get_org_info():
    req = request.get_json()
    orgId = req["orgId"]
    print("=" * 80)
    response = {
                "orgId": orgId,
                "name": "Roundpier",
                "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyUeJ6gwm221GHEsezMN1sfx6YKxH29urVndKAwS-P9Snir2XVKCjv1O1qXtg&",
                "topics" : ["topic1", "topic2"],
                }
    print(response)
    return jsonify(response)


@app.route('/get_reviews_topics', methods=['POST', 'GET'])
@cross_origin()
def get_reviews_topics():
    req = request.get_json()
    orgId = req["orgId"]
    print("=" * 80)
    response = {
                "orgId": orgId,
                "name": "Roundpier",
                "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyUeJ6gwm221GHEsezMN1sfx6YKxH29urVndKAwS-P9Snir2XVKCjv1O1qXtg&",
                "reviews" : [{"review" : "review1","topics" : ["topic1", "topic2"], "created_at" : "2021-10-12 20:29:03"},
                             {"review" : "review2","topics" : ["topic1", "topic3"], "created_at" : "2022-10-12 20:29:03"}],
                }
    print(response)
    return jsonify(response)

@app.route('/get_plot_data', methods=['POST', 'GET'])
@cross_origin()
def get_plot_data():
    req = request.get_json()
    orgId = req["orgId"]
    print("=" * 80)
    graph_data =  {
        "App Issues": [
            {
                "count": 2,
                "month": "2018-07"
            },
            {
                "count": 1,
                "month": "2018-09"
            },
            {
                "count": 1,
                "month": "2019-05"
            },
            {
                "count": 1,
                "month": "2019-12"
            },
            {
                "count": 1,
                "month": "2020-03"
            },
            {
                "count": 2,
                "month": "2020-06"
            },
            {
                "count": 1,
                "month": "2020-07"
            },
            {
                "count": 1,
                "month": "2020-10"
            },
            {
                "count": 1,
                "month": "2021-01"
            },
            {
                "count": 2,
                "month": "2021-06"
            }
        ],
        "Other Issues": [
            {
                "count": 2,
                "month": "2018-07"
            },
            {
                "count": 1,
                "month": "2020-02"
            },
            {
                "count": 1,
                "month": "2020-06"
            },
            {
                "count": 1,
                "month": "2022-01"
            }
        ]
    }
    graph_data_options = [
        {
            "name": "App Issues"
        },
        {
            "name": "Other Issues"
        }
    ]
    response = {
                "orgId": orgId,
                "name": "Roundpier",
                "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyUeJ6gwm221GHEsezMN1sfx6YKxH29urVndKAwS-P9Snir2XVKCjv1O1qXtg&",
                "plot_data" : {"graphData" : graph_data, "graphDataOptions" : graph_data_options},
                }
    print(response)
    return jsonify(response)



@app.route('/get_bugs', methods=['POST', 'GET'])
@cross_origin()
def get_bugs():

    query = request.args["brand"]

    response = bugs_detected_recommendations.handle_bugs(company=query.lower())
    print(response)
    return jsonify(response)

@app.route('/bugs', methods=['POST', 'GET'])
@cross_origin()
def bugs():
    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds)
    print(jwt_creds["username"])
    query = (jwt_creds["username"])
    response = bugs_detected_recommendations.handle_bugs(company=query.lower())
    print(response)
    return jsonify(response)

@app.route('/recommendations', methods=['POST', 'GET'])
@cross_origin()
def recommendations():

    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds)
    print(jwt_creds["username"])
    query = (jwt_creds["username"])

    response = bugs_detected_recommendations.handle_suggestions(company=query.lower())
    print(response)
    return jsonify(response)


@app.route('/graphs', methods=['POST', 'GET'])
@cross_origin()
def graphs():

    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds)
    print(jwt_creds["username"])
    query = (jwt_creds["username"])

    response = bugs_detected_recommendations.handle_bugs_watch_list(company=query.lower())
    print(response)
    return jsonify(response)



@app.route('/get_mix_graphs_data', methods=['POST', 'GET'])
@cross_origin()
def get_mix_graphs_data():

    query = request.args["brand"]

    response = bugs_detected_recommendations.handle_bugs_watch_list(company=query.lower())
    print(response)
    return jsonify(response)

@app.route('/getMixGraphsData', methods=['POST', 'GET'])
@cross_origin()
def getMixGraphsData():
    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds["username"])
    query = (jwt_creds["username"])

    response = bugs_detected_recommendations.handle_bugs_watch_list(company=query.lower())
    print(response)
    return jsonify(response)


@app.route('/get_recommendations', methods=['POST', 'GET'])
@cross_origin()
def get_suggestions():

    query = request.args["brand"]

    response = bugs_detected_recommendations.handle_suggestions(company=query.lower())
    print(response)
    return jsonify(response)


@app.route('/get_all_companies_in_db', methods=['POST', 'GET'])
@cross_origin()
def get_all_companies_in_db():

    all = read_write_db.get_all_data(TableName="company_handles")
    response = []
    for c in all:
        c["company_name"] =  c["company_name"].title()
        response.append(c)

    return jsonify(response)

@app.route('/add_company_integrations', methods=['POST', 'GET'])
@cross_origin()
def add_company_integrations():
    req = request.get_json()
    company_name = req["company_name"]
    playstore = req["playstore"]
    appstore = req["appstore"]
    twitter = req["twitter"]
    trustpilot = req["trustpilot"]
    req = get_handles_from_company_name(req["company_name"].lower())
    print(req)
    print("=" * 80)
    handlers2.handle_company_onboard(req)
    response = {
                "company_name": company_name,
                "playstore": playstore,
                "appstore": appstore,
                "twitter" : twitter,
                "trustpilot" : trustpilot,
                }
    print(response)
    return jsonify(response)

@app.route('/get_topics', methods=['POST', 'GET'])
@cross_origin()
def get_topics():
    query = request.args["brand"]
    table_name = "topics_" + query.lower()

    response = read_write_db.get_all_data(TableName=table_name)
    print(response)
    return jsonify(response)

@app.route('/getTopics', methods=['POST', 'GET'])
@cross_origin()
def getTopics():
    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds["username"])
    query = (jwt_creds["username"])
    table_name = "topics_" + query.lower()

    response = read_write_db.get_all_data(TableName=table_name)
    print(response)
    return jsonify(response)

@app.route('/add_topics', methods=['POST', 'GET'])
@cross_origin()
def add_topic():
    req = request.get_json()
    query = request.args["brand"]
    table_name = "topics_" + query.lower()

    print("=" * 80)
    print("adding topic")
    handlers2.handle_topics(req, table_name)

    response = {
                "topics": req,
                }
    print(response)
    return jsonify(response)


@app.route('/addTopic', methods=['POST', 'GET'])
@cross_origin()
def addTopic():
    req = request.get_json()
    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds["username"])
    query = (jwt_creds["username"])
    table_name = "topics_" + query.lower()
    table_name = "topics_" + query.lower()

    print("=" * 80)
    print("adding topic")
    handlers2.handle_topics(req, table_name)

    response = {
                "topics": req,
                }
    print(response)
    return jsonify(response)

@app.route('/remove_topic', methods=['POST', 'GET'])
@cross_origin()
def remove_topic():
    req = request.get_json()
    query = request.args["brand"]
    table_name = "topics_" + query.lower()

    topic = req["topic"]
    print(topic)
    print("=" * 80)
    handlers2.remove_topic(topic, table_name)

    response = {
                "topic": "topic",
                }


    print(response)
    return jsonify(response)

@app.route('/removeTopic', methods=['POST', 'GET'])
@cross_origin()
def removeTopic():
    req = request.get_json()
    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds["username"])
    query = (jwt_creds["username"])
    table_name = "topics_" + query.lower()

    topic = req["topic"]
    print(topic)
    print("=" * 80)
    handlers2.remove_topic(topic, table_name)

    response = {
                "topic": "topic",
                }


    print(response)
    return jsonify(response)


@app.route('/get_meta_data', methods=['POST', 'GET'])
@cross_origin()
def get_meta_data():
    req = request.get_json()

    query = request.args["brand"]

    response = get_playstore_meta_data("ksk")
    print(response)
    return jsonify(response)

import jwt_auth
@app.route('/login', methods=['POST', 'GET'])
@cross_origin()
def login():
    req = request.get_json()

    response = jwt_auth.check_login(req)
    orgdetails = handlers2.get_org_details_from_jwt(response["jwt"])
    response["org_details"] = orgdetails
    print(response)
    return jsonify(response)

from datetime import datetime

@app.route('/user_foot_print', methods=['POST', 'GET'])
@cross_origin()
def user_foot_print():
    req = request.get_json()
    item = {}
    item["data"] = str(req)
    item["ts"] = str(datetime.now())
    read_write_db.create_review(TableName="userFootPrints", item=item)
    print(req)
    return jsonify(req)

from collections import Counter
# import nltk
# from nltk.corpus import stopwords
# nltk.download('stopwords')
# from nltk.tokenize import word_tokenize



@app.route('/getWordCloud', methods=['POST', 'GET'])
@cross_origin()
def getWordCloud():

    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds["username"])
    query = (jwt_creds["username"])
    feedback_response, labels_sources, graph_data, graph_options = handlers2.get_dashboard_data(query)
    all_feedbacks = []
    response = []
    for feed in feedback_response:
        all_feedbacks.extend(feed["text"].lower().split(" "))
    remove = ["," , ")" , "-" , "." , "???" , "(" ,"app", "to" , "the" ,"in" , "and" , "this" , "it" , "but" , "a" , "for" , "is" , "was" , "my" , "i", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    for k, v in Counter(all_feedbacks).items():
        if k not in remove and v>1:
            response.append({"value" : k , "count" :v })

    print(response)
    return jsonify(response)


@app.route('/get_word_cloud3', methods=['POST', 'GET'])
@cross_origin()
def get_word_cloud3():
    query = request.args["brand"].lower()

    feedback_response, labels_sources, graph_data, graph_options = handlers2.get_dashboard_data(query)
    all_feedbacks = []
    response = []

    for feed in feedback_response:
        all_feedbacks.extend(feed["text"].lower().split(" "))
    remove = [",", ")", "-", ".", "???", "(", "app", "to", "the", "in", "and", "this", "it", "but", "a", "for", "is",
              "was", "my", "i", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
              "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
              "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
              "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having",
              "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
              "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during",
              "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
              "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any",
              "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same",
              "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    for k, v in Counter(all_feedbacks).items():
        if k not in remove and v > 1:
            response.append({"value": k, "count": v})
            # response.append({"text" : k , "value" :v })
    print(response)
    return jsonify(response)

@app.route('/get_word_cloud2', methods=['POST', 'GET'])
@cross_origin()
def get_word_cloud2():

    response = [
    {
        "count": 9,
        "value": "great"
    },
    {
        "count": 4,
        "value": "platform"
    }]
    print(response)
    return jsonify(response)


@app.route('/get_word_cloud', methods=['POST', 'GET'])
@cross_origin()
def get_word_cloud():
    # req = request.get_json()
    query = request.args["brand"].lower()

    feedback_response, labels_sources, graph_data, graph_options = handlers2.get_dashboard_data(query)
    all_feedbacks = []
    response = []

    for feed in feedback_response:
        all_feedbacks.extend(feed["text"].lower().split(" "))
    remove = ["," , ")" , "-" , "." , "???" , "(" ,"app", "to" , "the" ,"in" , "and" , "this" , "it" , "but" , "a" , "for" , "is" , "was" , "my" , "i", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    for k, v in Counter(all_feedbacks).items():
        if k not in remove and v>1:
            response.append({"value" : k , "count" :v })
            # response.append({"text" : k , "value" :v })
    print(response)
    return jsonify(response)



@app.route('/user', methods=['POST', 'GET'])
@cross_origin()
def user():
    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds["username"])
    response = handlers2.get_org_details(jwt_credentials=jwt_creds)

    print(response)
    return jsonify(response)


@app.route('/watchList', methods=['POST', 'GET'])
@cross_origin()
def watchList():
    jwt = request.headers.get('Authorization')
    jwt_creds = jwt_auth.read_active_jwts(jwt)
    print(jwt_creds)
    print(jwt_creds["username"])
    query = (jwt_creds["username"])
    response = watchlist.handle_wathcList(company_name=query.lower())

    print(response)
    return jsonify(response)


@app.route('/watch_list', methods=['POST', 'GET'])
@cross_origin()
def watch_list():
    print("in watch list")
    query = request.args["brand"].lower()
    print(query)
    response = watchlist.handle_wathcList(company_name=query.lower())

    print(response)
    return jsonify(response)


if __name__ == '__main__':
    # get_handles_from_company_name("deliveroo")
    app.run(host="0.0.0.0", port=8000)
