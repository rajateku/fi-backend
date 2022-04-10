import boto3
from boto3.dynamodb.conditions import Key


client = boto3.client('dynamodb' , region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')


def check_if_table_exists(TableName):
    existing_tables = dynamodb_client.list_tables()['TableNames']
    if TableName in existing_tables:
        return True
    else:
        return False


def create_table(TableName,key):
    existing_tables = dynamodb_client.list_tables()['TableNames']
    if TableName  in existing_tables:
        print("table exists  : {}".format(TableName))
        return "exists"
    else:

        table = dynamodb.create_table(
            TableName=TableName,
            KeySchema=[
                {
                    'AttributeName': key,
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': key,
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            }
        )

        print("Table status:", table.table_status)
        return table



def create_review(TableName, item):
    print("inside create review")
    table = dynamodb.Table(TableName)
    print(item)
    table.put_item(Item=item)
    print("item created")

    return "item created"

def delete_item(TableName, topic):
    table = dynamodb.Table(TableName)
    table.delete_item(Key={
            'topic': topic,
        })

    return "item deleted"


def get_company_handles(TableName, company_name):

    table = dynamodb.Table(TableName)

    resp = table.get_item(
        Key={
            'company_name': company_name,
        }
    )

    if 'Item' in resp:
        return (resp['Item'])
    else:
        return None


def get_all_data(TableName):
    table = dynamodb.Table(TableName)
    response = table.scan()

    return response['Items']

def get_column(TableName, column):
    table = dynamodb.Table(TableName)
    response = table.scan(AttributesToGet=[column])

    # response = table.scan()

    return response['Items']


if __name__ == '__main__':
    # # get_company_handles(TableName="company_handles", company_name = "dd" )
#     # items = get_all_data(TableName="userFootPrints")
#     # # print(items)
#     # for item in items:
#     #     print(item)
    companies = ["NHS", "Roundpier","Thursday",  "Transferwise", "Monzo", "Lyft", "Slack", "Dropbox", "Walmart", "Mediumcorporation"  ]
    # companies = [ "Mediumcorporation"  ]
    for c in companies:

        create_table(TableName= "topics_" + c.lower() , key="topic")
