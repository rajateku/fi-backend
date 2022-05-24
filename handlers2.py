import read_write_db
import download_save_appstore_data
import download_save_playstore_data
import download_save_trustpilot_db
import download_save_tweets_data

import get_playstore_data_db
import get_appstore_data_db
import get_trustpilot_data_db
import graphs
import time
from process_bugs_recos import handler_src_prc
import jwt_auth
import subprocess


def test_handlers():
    print("server working")
    return "server working with git push"


def scrape_all_4handles_data(company_name, playstore, appstore, twitter, trustpilot):
    print("appstore", appstore)

    TableNamePlayStore = "playstore_" + company_name.lower()
    TableNameAppStore = "appstore_" + company_name.lower()

    if twitter=="-" or twitter=="" or twitter==" ":
        print("passing twitter")
        pass
    else:
        TableNameTwitter = "twitter_" + company_name.lower()
        read_write_db.create_table(TableName=TableNameTwitter, key="id")

    TableNameTopics = "topics_" + company_name.lower()

    if trustpilot=="-" or trustpilot=="" or trustpilot==" ":
        print("passing trustiplot")
        pass
    else:
        TableNameTrustpilot = "trustpilot_" + company_name.lower()
        read_write_db.create_table(TableName=TableNameTrustpilot, key="created_at")

    read_write_db.create_table(TableName=TableNamePlayStore, key="reviewId")
    read_write_db.create_table(TableName=TableNameAppStore, key="date")
    read_write_db.create_table(TableName=TableNameTopics, key="topic")

    time.sleep(10)
    download_save_playstore_data.scrape(query=playstore, table_name= TableNamePlayStore)
    download_save_appstore_data.scrape(query=appstore, table_name= TableNameAppStore)


    if twitter=="-" or twitter=="" or twitter==" ":
        print("inside twitter download pass")
        pass
    else:
        download_save_tweets_data.search_and_save_twitter(twitter, table_name=TableNameTwitter)

    if trustpilot=="-" or trustpilot=="" or trustpilot==" ":
        print("inside trustpilot pass download")
        pass
    else:
        download_save_trustpilot_db.scrape(trustpilot, table_name=TableNameTrustpilot)


def handle_process_data(company_name):
    handler_src_prc.source_data_to_processed_table(company_name)


def handle_company_onboard(req):
    company_name = req["company_name"]
    playstore = req["playstore"]
    appstore = req["appstore"]
    twitter = req["twitter"]
    trustpilot = req["trustpilot"]
    req["company_name"] = req["company_name"].lower()

    read_write_db.create_table(TableName="company_handles", key=company_name)
    read_write_db.create_review(TableName="company_handles", item=req)

    scrape_all_4handles_data(company_name = company_name, playstore = playstore, appstore = appstore, twitter = twitter, trustpilot = trustpilot)
    # source_data_to_processed_table(company_name=company_name)
    # handler_src_prc.source_data_to_processed_table("roundpier")
    handle_process_data(company_name)
    # subprocess.run(["python", "process_bugs_recos/handler_src_prc.py" , company_name.lower()])



def get_dashboard_data(company_name):
    processedTableName = "processed_" + company_name.lower()

    feedback_response  = read_write_db.get_all_data(TableName=processedTableName)
    feedback_response = sorted(feedback_response, key=lambda k: k.get('created_at', 0), reverse=True)

    graph_data, graph_options = graphs.get_graph_data_from_response(feedback_response)
    labels_sources = [ "Twitter" , "App Store" , "Play Store", "Trustpilot"]
    topic_labels_dashboard = read_write_db.get_all_data(TableName="topics_" + company_name.lower())
    labels_sources =  labels_sources + [a ["topic"] for a in topic_labels_dashboard]

    return feedback_response , labels_sources, graph_data, graph_options


def source_data_to_processed_table(company_name):
    print("In source_data_to_processed_table")
    TableNamePlayStore = "playstore_" + company_name.lower()
    TableNameAppStore = "appstore_" + company_name.lower()
    TableNameTrustpilot = "trustpilot_" + company_name.lower()

    processedTableName = "processed_" + company_name.lower()
    check = read_write_db.create_table(TableName=processedTableName, key="created_at" )

    topics = read_write_db.get_all_data(TableName="topics")

    if check == "exists":
        pass
    else:
        time.sleep(10)

    if read_write_db.check_if_table_exists(TableNamePlayStore):
        playstore_reponse, count_labels_playstore = get_playstore_data_db.get_data_from_db_processed(
            TableName=TableNamePlayStore, topics=topics)
        for review in playstore_reponse:
            read_write_db.create_review(TableName= processedTableName, item=review)

    if read_write_db.check_if_table_exists(TableNameAppStore):
        appstore_reponse, count_labels_appstore = get_appstore_data_db.get_data_from_db_processed(
            TableName=TableNameAppStore, topics=topics)
        for review in appstore_reponse:
            read_write_db.create_review(TableName= processedTableName, item=review)

    if read_write_db.check_if_table_exists(TableNameTrustpilot):
        trustpilot_reponse, count_labels_trustpilot = get_trustpilot_data_db.get_data_from_db_processed(
            TableName=TableNameTrustpilot, topics=topics)
        for review in trustpilot_reponse:
            read_write_db.create_review(TableName= processedTableName, item=review)
    print("source_data_to_processed_table finished")


def handle_topics(req, table_name):
    print("inside handle_topics")
    read_write_db.create_table(TableName=table_name, key="topic")
    for topic in req:
        read_write_db.create_review(TableName=table_name, item=topic)
    handle_process_data(table_name.replace("topics_", ""))
    print("finished handle_topics")

    # company = "roundpier"
    # source_data_to_processed_table(company)
    # print("source_data_to_processed_table Finished")


def handle_bugs(company):
    print("inside handle_bugs")
    all_data = read_write_db.get_all_data(TableName="processed_" + company)
    bugs_data = []
    for review in all_data:
        if review["highlightText"] =="":
            pass
        else:
            bugs_data.append(review)
    bugs_data = sorted(bugs_data, key=lambda k: k.get('created_at', 0), reverse=True)

    print("finished handle_bugs")

    return bugs_data


def remove_topic(topic, table_name):
    print("inside handle_topics")
    # for topic in req:
    read_write_db.delete_item(TableName=table_name, topic=topic)
    print("finished handle_topics")


def get_org_details(jwt_credentials):
    print("inside handle_topics")
    response = ""
    companies = read_write_db.get_all_data(TableName="company_handles")
    for company in companies:
        if company["company_name"] ==jwt_credentials["username"]:
            response = company

    print("finished handle_topics")
    return response

def get_org_details_from_jwt(jwt):
    org_username = jwt_auth.read_active_jwts(jwt)
    print("inside company_handles")
    response = ""
    companies = read_write_db.get_all_data(TableName="company_handles")
    for company in companies:
        if company["company_name"] ==org_username["username"]:
            response = company

    print("finished handle_topics")
    return response


if __name__ == '__main__':

    company = "roundpier"
    #
    #
    # # companies = [ "nhs" , "lyft" , "monzo" ,]
    # companies = [ "nhs" , "lyft" , "monzo" , "roundpier" ,  "transferwise" , "walmart" , "slack" , "dropbox" , "mediumcorporation" ]
    #
    # # for company in companies:
    # #     # source_data_to_processed_table(company)
    #     # get_dashboard_data(company)
    handle_process_data(company)

    # subprocess.run(["python", "process_bugs_recos/handler_src_prc.py" , company])

