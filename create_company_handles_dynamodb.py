

import boto3

client = boto3.client('dynamodb' , region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


TableName = 'company_handles'


def create_trustpilot_table():
    table = dynamodb.create_table(
        TableName=TableName,
        KeySchema=[
            {
                'AttributeName': 'company_name',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'company_name',
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

# trustpilot_table = create_trustpilot_table()


def create_company_handle(item):
    print(
        "inside handles"
    )
    table = dynamodb.Table(TableName)
    table.put_item(Item=item)

    return "company handles created"


