# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

from app_store_scraper import AppStore
import datetime
import read_write_db


#
# def form_better_dataframes(search_tweets):
#     search_tweets_with_location = []
#
#     for tweet in search_tweets["data"]:
#         for user in search_tweets["includes"]["users"]:
#             if user[ID] == tweet[AUTHOR_ID] and LOCATION in user:
#                 print(tweet, tweet[AUTHOR_ID], user[ID], user[LOCATION])
#                 tweet[LOCATION] = user[LOCATION]
#                 search_tweets_with_location.append(tweet)
#     df = pd.DataFrame(search_tweets_with_location)
#     return df


# def save_file_to_local(query, search_result):
#     if search_result.json()["meta"]["result_count"] == 0:
#         return {"data": [{TEXT: "No results", "polarity": ""}]}
#
#     json_response_df = form_better_dataframes(search_result.json())
#     CSV_FILE = CSV_FOLDER + "{}.csv".format(query)
#     print(json_response_df)
#     json_response_df[[TEXT, ID, LOCATION, CREATED_AT]].to_csv(CSV_FILE, mode="a", index=False)
#
#     data_overall_df = pd.read_csv(CSV_FILE, index_col=None)
#     with open(CSV_FILE, "r") as f:
#         reader = csv.DictReader(f)
#         a = list(reader)
#
#     return {
#         "data": a
#     }


def scrape(query, table_name):
    print("appstore query : ", query)
    app_name = query.split("_")[0]
    id = query.split("_")[1]
    print("Scraping appstore reviews")
    appstore_response = AppStore(country='us', app_name=app_name, app_id=id)

    # appstore_response.review(how_many=100, after=datetime.datetime(2022, 1, 1))
    appstore_response.review(how_many=10)

    app_reviews = appstore_response.reviews
    for review in app_reviews:
        review["date"] = str(review["date"])
        read_write_db.create_review(table_name, item=review)
    print(len(app_reviews))
    # CSV_FILE = "Data4/{}.csv".format(appstore_query)
    # #
    # df = pd.DataFrame(np.array(app_reviews), columns=['review'])
    # df_reviews = df.join(pd.DataFrame(df.pop('review').tolist()))
    # #
    # # print(df2.head())
    # try:
    #
    #     df1 = pd.read_csv(CSV_FILE)
    #     print(df1)
    #     print(df_reviews)
    #     df_all = pd.concat([df1, df_reviews]).drop_duplicates(ignore_index=True)
    #     df_final = df_all.drop_duplicates(subset=['reviewId'])
    #     df_final.to_csv(CSV_FILE, mode="a", index=False)
    #     print("try")
    #
    #
    # # past_df.append(df_busu).drop_duplicates().to_csv(CSV_FILE, mode="a").reset_index(drop=True)
    # except:
    #     df_reviews.to_csv(CSV_FILE, mode="a", index=False)
    #     print("except")
    # print(df2)




    # return df2

if __name__ == '__main__':
    appstore_handle = "wise_612261027"
    TableName = "appstore_wise"
    read_write_db.create_table(TableName=TableName, key="date")
    query = appstore_handle
    json_response = scrape(appstore_handle, table_name=TableName)
