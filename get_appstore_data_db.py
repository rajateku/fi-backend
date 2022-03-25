from logging_python import logger
import boto3
import get_labels
from handlers import prepare_labels_strip_navigation
dynamodb = boto3.resource('dynamodb')


def prepare_response_object_from_appstore_files(file_data):
    response = []
    labels = []

    for i, review in enumerate(file_data, start=1):
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
            # REVIEW_OBJECT["id"] = str(i)
            REVIEW_OBJECT["title"] = review["title"]
            REVIEW_OBJECT["text"] = review["review"]
            REVIEW_OBJECT["location"] = ""
            REVIEW_OBJECT["created_at"] = review["date"]
            REVIEW_OBJECT["labels"] = [get_labels.review_to_topic(str(review["review"]))]
            REVIEW_OBJECT["highlightText"]= get_labels.review_to_highlight(str(review["review"]))
            REVIEW_OBJECT["labels"].append("appstore")
            REVIEW_OBJECT["labels"].append( str(review["rating"]))
            REVIEW_OBJECT["rating"] = str(review["rating"])
            REVIEW_OBJECT["url"] = ""

            labels.extend(REVIEW_OBJECT["labels"])
            response.append(REVIEW_OBJECT)

    labels_strip = prepare_labels_strip_navigation(labels)

    return response, labels_strip


def get_data_from_db_processed(TableName):

    logger.info("connecting to db")
    table = dynamodb.Table(TableName)
    # response = table.scan(ProjectionExpression="review, rating")
    response = table.scan()

    # print(response['Items'])
    resp = prepare_response_object_from_appstore_files(response['Items'])
    return resp


if __name__ == '__main__':
    TableName = "appstore_wise"
    json_response = get_data_from_db_processed(TableName)
