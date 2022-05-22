import boto3
import process_bugs_recos.get_labels as get_labels

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


def prepare_response_object_from_playstore_files(file_data, topics):
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
        REVIEW_OBJECT["labels"] = get_labels.review_to_topic(str(review["content"]), topics)
        REVIEW_OBJECT["highlightText"] = get_labels.review_to_highlight(str(review["content"]))
        REVIEW_OBJECT["suggestionText"] = get_labels.review_to_suggestion(str(review["content"]))
        REVIEW_OBJECT["labels"].append("Play Store")
        REVIEW_OBJECT["labels"].append(str(review["score"]))
        response.append(REVIEW_OBJECT)
        labels.extend(REVIEW_OBJECT["labels"])


    return response


def get_data_from_db_processed(TableName, topics):

    table = dynamodb.Table(TableName)
    # response = table.scan(ProjectionExpression="review, rating")
    response = table.scan()

    # print(response['Items'])
    resp = prepare_response_object_from_playstore_files(response['Items'], topics)
    return resp


if __name__ == '__main__':
    TableName = "playstore_roundpier"
    json_response = get_data_from_db_processed(TableName)
