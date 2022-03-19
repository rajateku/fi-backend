import csv
import os
# from  negation_from_sentence import gieven_sentence_give_chunk
from review_topics_map  import review_to_topic
CSV_FOLDER = "/Users/rajateku/Documents/ACADEMICS/PROJECT/rt257/code/Data4/"


def get_data_from_csv_file(query):
    CSV_FILE = CSV_FOLDER + "{}.csv".format(query)

    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        print(reader)
        a = list(reader)

    response = {"data": a}
    return response


def check_if_review_contains_negation(text):
    sentences = text.split(". ")
    bugs = []
    for s in sentences:
        text = s
        print(text)
        gieven_sentence_give_chunk(s)
    #     if text.__contains__("can't") or text.__contains__("wont") or text.__contains__("unable") or text.__contains__("cannot"):
    #         bugs.append(text)
    #         # return True,
    #     # else:
    #         # return False
    # print(bugs)
    return False

for filename in ["wise_612261027.csv"]:
# for filename in os.listdir(CSV_FOLDER):
    f = os.path.join(CSV_FOLDER, filename)
    if os.path.isfile(f) and filename.__contains__("_"):

        print(filename.replace(".csv", ""))
        appstore_handle = (filename.replace(".csv", ""))
        query = appstore_handle
        json_response = get_data_from_csv_file(query=query)

        for review in json_response["data"]:
            # print("="*60)
            try:
                if int(review["rating"])<4:
                    print("=" * 70 + review["title"] + "=" * 60)
                    # flag = check_if_review_contains_negation(review["review"])

                    print(review["rating"])
                    # print(review["review"])
                    _, topic = review_to_topic(review["review"])
                    print("topic : ", topic)
            except:
                pass


# appstore_handle = "wise_612261027"
# # appstore_handle = "roundpier_1400305303"
# json_response = get_data_from_csv_file(query=appstore_handle)
# for review in json_response["data"]:
#     print("="*60)
#     if int(review["rating"])< 3:
#         print("="*70 + review["title"] + "="*60)
#         print(review["rating"])
#         print(review["review"])
