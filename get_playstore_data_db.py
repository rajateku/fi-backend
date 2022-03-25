from logging_python import logger
import boto3
import get_labels
from handlers import prepare_labels_strip_navigation
dynamodb = boto3.resource('dynamodb')


def prepare_response_object_from_playstore_files(file_data):
    response = []
    labels = []

    for i, review in enumerate(file_data):
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

        # REVIEW_OBJECT["id"] = str(i)
        REVIEW_OBJECT["text"] = review["content"]
        REVIEW_OBJECT["location"] = ""
        REVIEW_OBJECT["created_at"] = review["at"]
        REVIEW_OBJECT["rating"] = str(review["score"])
        REVIEW_OBJECT["labels"] = [get_labels.review_to_topic(str(review["content"]))]
        REVIEW_OBJECT["highlightText"] = get_labels.review_to_highlight(str(review["content"]))
        REVIEW_OBJECT["labels"].append("playstore")
        REVIEW_OBJECT["labels"].append(str(review["score"]))
        response.append(REVIEW_OBJECT)
        labels.extend(REVIEW_OBJECT["labels"])

    labels_strip = prepare_labels_strip_navigation(labels)

    return response, labels_strip


def get_data_from_db_processed(TableName):

    logger.info("connecting to db")
    table = dynamodb.Table(TableName)
    # response = table.scan(ProjectionExpression="review, rating")
    response = table.scan()

    # print(response['Items'])
    resp = prepare_response_object_from_playstore_files(response['Items'])
    return resp


if __name__ == '__main__':
    TableName = "playstore_roundpier"
    json_response = get_data_from_db_processed(TableName)
