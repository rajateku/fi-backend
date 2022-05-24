from logging_python import logger
import boto3
import process_bugs_recos.get_labels as get_labels
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')



def prepare_response_object_from_trustpilot_db(file_data, topics):
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
                "highlightText": "",
                "source": "Trustpilot"
            }
            # REVIEW_OBJECT["id"] = str(i)
            # print("review trustpilot :" , review)
            REVIEW_OBJECT["text"] = review["content"]
            REVIEW_OBJECT["title"] = review["title"]
            REVIEW_OBJECT["location"] = ""
            REVIEW_OBJECT["created_at"] = review["created_at"]
            REVIEW_OBJECT["labels"] = get_labels.review_to_topic(str(review["content"]), topics)
            REVIEW_OBJECT["highlightText"] = get_labels.review_to_highlight(str(review["content"]))
            REVIEW_OBJECT["suggestionText"] = get_labels.review_to_suggestion(str(review["content"]))
            REVIEW_OBJECT["labels"].append("Trustpilot")
            REVIEW_OBJECT["labels"].append(str(review["rating"]))
            REVIEW_OBJECT["rating"] = str(review["rating"].split(" ")[1])
            REVIEW_OBJECT["url"] = ""

            labels.extend(REVIEW_OBJECT["labels"])
            response.append(REVIEW_OBJECT)
    # labels_strip = prepare_labels_strip_navigation(labels)

    return response


def get_data_from_db_processed(TableName, topics):

    logger.info("connecting to db")
    table = dynamodb.Table(TableName)
    # response = table.scan(ProjectionExpression="review, rating")
    response = table.scan()
    resp = prepare_response_object_from_trustpilot_db(response['Items'], topics)
    return resp


if __name__ == '__main__':
    TableName = "trustpilot_deliveroo"
    topics = {}
    json_response = get_data_from_db_processed(TableName)
