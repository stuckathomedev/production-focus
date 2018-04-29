from datetime import date

import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Tasks')


def table_item_count():
    print(table.item_count)


def table_creation_time():
    print(table.creation_time)


def create_task(id, user_id, description, is_recurring, days_until, due_time):
    table.put_item(
        Item={
            'CustomerID': str(id),
            'user_id': user_id,
            'description': description,
            'is_recurring': is_recurring,
            'completed': False,
            'last_completed': str(date.today()),
            'days_until': days_until, # The number of days until the reminder triggers
            'due_time': str(due_time), # The specific time that the reminder should be triggered
            'completions': 0, # How many times one has completed the scheduled task
            'trials': 0, # The number of times that the task has executed
        }
    )

def search_task(id):
    response = table.get_item(
        Key={
            'CustomerID': id
        }
    )
    item = response['Item']
    print(item)


def update_intent(id, **kwargs):
    for key, value in kwargs.items():
        table.update_item(
            Key={
                'CustomerID': id
            },
            UpdateExpression=f'SET {key} = :vary',
            ExpressionAttributeValues={
                ':vary': value
            }
        )

def get_all_tasks():
    # TODO paginate when tasks > 1 MB
    return table.scan(
        Select='ALL_ATTRIBUTES',
        ConsistentRead=True
    )['Items']


def delete_intent(id):
    table.delete_item(
        Key={
            'CustomerID': id
        }
    )

def search_by_user(user_id):
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    item = response['Item']
    print(item)
    return(item)