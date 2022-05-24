import sys
# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.insert(1, 'p')

import process_bugs_recos.read_write_db2 as read_write_db
import process_bugs_recos.get_playstore_data_db2 as get_playstore_data_db
import process_bugs_recos.get_appstore_data_db as get_appstore_data_db


import process_bugs_recos.get_trustpilot_data_db as get_trustpilot_data_db
import process_bugs_recos.get_tweets_data_from_db as get_tweets_data_from_db


import time

def source_data_to_processed_table(company_name):

    print("In source_data_to_processed_table")
    TableNamePlayStore = "playstore_" + company_name.lower()
    TableNameAppStore = "appstore_" + company_name.lower()

    TableNameTrustpilot = "trustpilot_" + company_name.lower()
    TableNameTwitter = "twitter_" + company_name.lower()

    processedTableName = "processed_" + company_name.lower()

    check = read_write_db.create_table(TableName=processedTableName, key="created_at" )

    if check == "exists":
        pass
    else:
        time.sleep(10)

    topics = read_write_db.get_all_data(TableName="topics_" + company_name.lower())
    print("topics : ", topics )


    if read_write_db.check_if_table_exists(TableNamePlayStore):
        playstore_reponse = get_playstore_data_db.get_data_from_db_processed(
            TableName=TableNamePlayStore, topics=topics)
        print((playstore_reponse))
        for review in playstore_reponse:
            read_write_db.create_review(TableName= processedTableName, item=review)

    if read_write_db.check_if_table_exists(TableNameTwitter):
        appstore_reponse = get_tweets_data_from_db.get_data_from_db_processed(
            TableName=TableNameTwitter, topics=topics)
        for review in appstore_reponse:
            read_write_db.create_review(TableName= processedTableName, item=review)

    if read_write_db.check_if_table_exists(TableNameTrustpilot):
        appstore_reponse = get_trustpilot_data_db.get_data_from_db_processed(
            TableName=TableNameTrustpilot, topics=topics)
        for review in appstore_reponse:
            read_write_db.create_review(TableName= processedTableName, item=review)

    if read_write_db.check_if_table_exists(TableNameAppStore):
        appstore_reponse = get_appstore_data_db.get_data_from_db_processed(
            TableName=TableNameAppStore, topics=topics)
        for review in appstore_reponse:
            read_write_db.create_review(TableName= processedTableName, item=review)

    print("source_data_to_processed_table finished")





if __name__ == '__main__':

    # company = "roundpier"

    # companies = ["nhs" ]
    # "NHS", "Roundpier", "Transferwise", "Deliveroo", "Monzo", "Lyft", "Slack", "Dropbox", "Walmart", "Mediumcorporation"
    # companies = [ "nhs" , "lyft" , "monzo" , "roundpier" ,  "transferwise" , "walmart" , "slack" , "dropbox" , "mediumcorporation" ]
    # companies = [   "transferwise" , "walmart" , "slack" , "dropbox" ]
    # companies = [  "thursday"  ]
    # companies = [  "allsetnow"  ]

    companies = [  "roundpier"  ]
    import sys

    print("This is the name of the program:", sys.argv[0])

    print("Argument List:", str(sys.argv))
    for company in companies:
        # source_data_to_processed_table(sys.argv[1])
        source_data_to_processed_table("deliveroo")
