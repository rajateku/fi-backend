# import download_save_tweets_data
import download_save_playstore_data
import download_save_appstore_data

import get_tweets_data_from_files
import get_google_playstore_data_from_files
import get_apple_appstore_data_from_files
import get_trustpilot_data_from_files

import get_labels
import graphs
# import get_sentiment

import os
from collections import Counter
from logging_python import logger

TWITTER_QUERY = "@Deliveroo"
PLAYSTORE_QUERY = "com.deliveroo.orderapp"
SECTORS = ["tech", "food", "delivery"]


def prepare_response_object_from_twitter_files(file_data, sectors):
    response = []
    labels = []
    for i, tweet in enumerate(file_data["data"]):
        REVIEW_OBJECT = {
            "id": "",
            "text": "",
            "location": "",
            "url": "",
            "labels": "",
            "sentiment": "",
            "highlightText": "",
            "source" : "twitter"

        }

        REVIEW_OBJECT["id"] = i
        REVIEW_OBJECT["text"] = tweet["text"]
        REVIEW_OBJECT["location"] = tweet["location"]
        REVIEW_OBJECT["created_at"] = tweet["created_at"]
        REVIEW_OBJECT["rating"] = "0"
        # REVIEW_OBJECT["labels"] = get_labels.given_sentence_to_lables(str(tweet["text"]), sectors)
        REVIEW_OBJECT["labels"] = [get_labels.review_to_topic(str(tweet["text"]))]
        REVIEW_OBJECT["highlightText"] = get_labels.review_to_highlight(str(tweet["text"]))
        REVIEW_OBJECT["labels"].append("twitter")
        print(REVIEW_OBJECT["labels"])
        # REVIEW_OBJECT["sentiment"] = get_sentiment.give_sentiment(str(tweet["text"]))
        REVIEW_OBJECT["url"] = "https://twitter.com/bradfordeurope/status/" + tweet["id"]
        response.append(REVIEW_OBJECT)
        labels.extend(REVIEW_OBJECT["labels"])

    labels_strip = prepare_labels_strip_navigation(labels)

    return response, labels_strip


def prepare_response_object_from_playstore_files(file_data, sectors):
    response = []
    labels = []

    for i, review in enumerate(file_data["data"]):
        REVIEW_OBJECT = {
            "id": "",
            "text": "",
            "location": "",
            "url": "",
            "labels": "",
            "sentiment": "",
            "highlightText": "",
            "source": "playstore"
        }

        REVIEW_OBJECT["id"] = i
        REVIEW_OBJECT["text"] = review["content"]
        REVIEW_OBJECT["location"] = ""
        REVIEW_OBJECT["created_at"] = review["at"]
        REVIEW_OBJECT["rating"] = review["score"]
        REVIEW_OBJECT["labels"] = [get_labels.review_to_topic(str(review["content"]))]
        REVIEW_OBJECT["highlightText"] = get_labels.review_to_highlight(str(review["content"]))
        REVIEW_OBJECT["labels"].append("playstore")
        REVIEW_OBJECT["labels"].append(str(review["score"]))

        # REVIEW_OBJECT["labels"] = get_labels.given_sentence_to_lables(str(review["content"]), sectors)
        # REVIEW_OBJECT["sentiment"] = get_sentiment.give_sentiment(str(review["content"]))
        REVIEW_OBJECT["url"] = "https://play.google.com/store/apps/details?id=" + PLAYSTORE_QUERY
        response.append(REVIEW_OBJECT)
        labels.extend(REVIEW_OBJECT["labels"])

    labels_strip = prepare_labels_strip_navigation(labels)

    return response, labels_strip


def prepare_response_object_from_appstore_files(file_data, sectors, appstore_query):
    response = []
    labels = []
    # date_count = []

    for i, review in enumerate(file_data["data"], start=1):
        # if int(review["rating"])<4:
            REVIEW_OBJECT = {
                "id": "",
                "text": "",
                "title": "",
                "location": "",
                "url": "",
                "labels": "",
                "sentiment": "",
                "rating": "",
                "highlightText" : "",
                "source": "appstore"
            }
            REVIEW_OBJECT["id"] = i
            REVIEW_OBJECT["title"] = review["title"]
            REVIEW_OBJECT["text"] = review["review"]
            REVIEW_OBJECT["location"] = ""
            REVIEW_OBJECT["created_at"] = review["date"]
            # REVIEW_OBJECT["labels"] = list(set(get_labels.given_sentence_to_lables(str(review["review"]), sectors)))
            REVIEW_OBJECT["labels"] = [get_labels.review_to_topic(str(review["review"]))]
            REVIEW_OBJECT["highlightText"]= get_labels.review_to_highlight(str(review["review"]))
            REVIEW_OBJECT["labels"].append("appstore")
            REVIEW_OBJECT["labels"].append( str(review["rating"]))

    # REVIEW_OBJECT["sentiment"] , _ = get_sentiment.give_sentiment(str(review["review"]))
            REVIEW_OBJECT["rating"] = str(review["rating"])
            REVIEW_OBJECT["url"] = ""
            # REVIEW_OBJECT["labels"].append(str(review["rating"]) + " star")
            date_issue_count = [{"month" : "" , "issue": "" , "count": ""}]

            # date_issue_count["issue"] =
            # if get_labels.review_to_topic(str(review["review"])) == "Extra fees issue" :
            #     print(review["date"][:7])
            #     date_count.append(review["date"][:7])

            # print(Counter(date_count))
            labels.extend(REVIEW_OBJECT["labels"])


            response.append(REVIEW_OBJECT)
            # logger.info('REVIEW_OBJECT["labels"]')
            # logger.info(REVIEW_OBJECT["labels"])
    # for date,count in Counter(date_count).items():
    #     print(date, count)


    labels_strip = prepare_labels_strip_navigation(labels)
    # print(response)

    return response, labels_strip


def prepare_labels_strip_navigation(labels):
    count_labels_strip = []
    logger.info("labels")
    # logger.info(labels)
    count_labels = dict(Counter((labels)))

    # count_labels = sorted(labels)
    logger.info(str(count_labels))

    for count_label, value in count_labels.items():
        count_labels_strip.append(str(count_label) + "(" + str(value) + ")")
    # count_labels_strip.append("all")
    logger.info("count_labels_strip : " + str(count_labels_strip))

    return count_labels_strip


def check_if_file_exists(query):
    CSV_FOLDER = "Data4/"
    if os.path.exists(CSV_FOLDER + query + ".csv"):
        return True
    else:
        return False


def handle_request(twitter_query, playstore_query, appstore_query, trustpilot_query,  sectors=None):
    print("twitter_query")
    print(twitter_query)
    if twitter_query=="-":
        print("passing")
        pass
    else:
        flag = check_if_file_exists(twitter_query)
        if flag:
            pass
        else:
            download_save_tweets_data.search_and_save_twitter(twitter_query)



    flag = check_if_file_exists(playstore_query)
    if flag:
        pass
    else:
        download_save_playstore_data.scrape(playstore_query)

    flag = check_if_file_exists(appstore_query)
    if flag:
        pass
    else:
        logger.info("APPSTORE - Downloading and saving file....")
        download_save_appstore_data.scrape(appstore_query)

    if twitter_query=="-":
        twitter_reponse = []
        count_labels_twitter = []
    else:
        tweets_response = get_tweets_data_from_files.get_data_from_csv_file(twitter_query)
        print("got tweets file data - twitter")
        twitter_reponse, count_labels_twitter = prepare_response_object_from_twitter_files(tweets_response, sectors)
        print(twitter_reponse)


    reviews_response = get_google_playstore_data_from_files.get_data_from_csv_file(playstore_query)
    print("got reviews file data -playstore")
    playstore_reponse, count_labels_playstore = prepare_response_object_from_playstore_files(reviews_response, sectors)
    # print(playstore_reponse)

    reviews_response = get_apple_appstore_data_from_files.get_data_from_csv_file(appstore_query)
    logger.info("APPSTORE - got reviews file data")
    appstore_reponse, count_labels_appstore = prepare_response_object_from_appstore_files(reviews_response, sectors,
                                                                                 appstore_query)

    logger.info("trustpilotquery")
    logger.info(trustpilot_query)
    if trustpilot_query == "-":
        trustpilot_reponse = []
    else:
        trustpilot_reponse = get_trustpilot_data_from_files.get_data_from_json_files(trustpilot_query)

    labels_sources = ["trustpilot" , "twitter" , "appstore" , "playstore"]
    feedback_response = appstore_reponse + playstore_reponse
    count_labels  =  labels_sources + count_labels_appstore + count_labels_twitter + count_labels_playstore
    # count_labels  =  labels_sources
    feedback_response = sorted(feedback_response, key=lambda k: k.get('created_at', 0), reverse=True)
    graph_data, graph_options = graphs.get_graph_data_from_response(feedback_response)



    return feedback_response + twitter_reponse + trustpilot_reponse , count_labels, graph_data, graph_options


if __name__ == '__main__':
    APPSTORE_QUERY = "wise_612261027"
    handle_request(TWITTER_QUERY, PLAYSTORE_QUERY,APPSTORE_QUERY, sectors=SECTORS)
    # flag = check_if_file_exists("tiktok_835599320")
    # print(flag)
