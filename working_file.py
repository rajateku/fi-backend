import pandas as pd
# import get_sentiment
# import get_labels

#
# df = pd.read_csv("bolt_play_store_reviews.csv")
# sector_list = ["riding", "tech"]
# print(df["Reviews"])
# reviews = df["Reviews"]
#
# for review in reviews:
#     review = str(review)
#     sentiment = get_sentiment.give_sentiment(review)
#     labels = get_labels.given_sentence_to_lables(review, sector_list)
#     print(review, sentiment, labels)


def get_handles_from_company_name(company_lower_case):
    df = pd.read_csv("Company Reviews - handles.csv")
    row = df.loc[df["Company_lower_case"] == company_lower_case]
    # print(row)
    print(row["Playstore"].values[0])
    playstore_query = row["Playstore"].values[0]
    appstore_name, appstore_id = str(row["Appstore"].values[0]).split("/id")
    appstore_query = appstore_name + "_"+ appstore_id
    twitter_query = str(row["Twitter"].values[0])
    print(playstore_query, appstore_query, twitter_query)
    # print(playstore_query)
    return appstore_query

get_handles_from_company_name("deliveroo")
get_handles_from_company_name("bolt")