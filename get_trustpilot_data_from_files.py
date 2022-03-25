import csv
from logging_python import logger
import os
import json
import get_labels

FILES_FOLDER = "data_jsons/"
if os.path.exists(FILES_FOLDER):
    pass
else:
    os.mkdir(FILES_FOLDER)

def get_all_json_files_starting_with_query(query):
    ls_files = os.listdir(FILES_FOLDER)
    files = []
    for file in ls_files:
        if file.startswith(query):
            files.append(file)
    logger.info(files)
    return files




def prepare_response_object_from_appstore_files(file_data):
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
                "highlightText": "",
                "source": "trustpilot"
            }
            REVIEW_OBJECT["id"] = i
            REVIEW_OBJECT["text"] = review["content"]
            REVIEW_OBJECT["title"] = review["title"]
            REVIEW_OBJECT["location"] = ""
            REVIEW_OBJECT["created_at"] = review["created_at"]
            # REVIEW_OBJECT["labels"] = list(set(get_labels.given_sentence_to_lables(str(review["review"]), sectors)))
            REVIEW_OBJECT["labels"] = [get_labels.review_to_topic(str(review["content"]))]
            REVIEW_OBJECT["highlightText"] = get_labels.review_to_highlight(str(review["content"]))
            REVIEW_OBJECT["labels"].append("trustpilot")
            REVIEW_OBJECT["labels"].append(str(review["rating"]))

            REVIEW_OBJECT["rating"] = str(review["rating"].split(" ")[1])
            REVIEW_OBJECT["url"] = ""

            labels.extend(REVIEW_OBJECT["labels"])


            response.append(REVIEW_OBJECT)
            # logger.info('REVIEW_OBJECT["labels"]')
            # logger.info(REVIEW_OBJECT["labels"])
    # for date,count in Counter(date_count).items():
    #     print(date, count)
    # print(response)

    return response


def get_data_from_json_files(query):
    json_files = get_all_json_files_starting_with_query(query)
    for json_file in json_files:
        f = open(FILES_FOLDER + "/"+ json_file)
        data = json.load(f)
    # print(data)
    data = {"data" : data}

    response = prepare_response_object_from_appstore_files(data)
    return response


if __name__ == '__main__':
    query = "www.deliveroo.co.uk"
    json_response = get_data_from_json_files(query=query)
    # get_all_json_files_starting_with_query(query)
