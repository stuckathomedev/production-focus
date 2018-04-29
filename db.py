from datetime import date

import boto3

dynamodb = boto3.resource('dynamodb')

tasks = dynamodb.Table('Tasks')
phone_numbers = dynamodb.Table('PhoneNumbers')


def table_item_count():
    print(tasks.item_count)


def table_creation_time():
    print(tasks.creation_time)


def create_task(task_id, user_id, description, is_recurring, days_until, due_time):
    tasks.put_item(
        Item={
            'task_id': str(task_id),
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

def get_task(user_id, task_id):
    response = tasks.get_item(
        Key={
            'user_id': user_id,
            'task_id': task_id
        }
    )
    item = response['Item']
    print(item)


def update_task(user_id, task_id, **kwargs):
    for key, value in kwargs.items():
        tasks.update_item(
            Key={
                'user_id': user_id,
                'task_id': task_id
            },
            UpdateExpression=f'SET {key} = :vary',
            ExpressionAttributeValues={
                ':vary': value
            }
        )

def get_all_tasks():
    # TODO paginate when tasks > 1 MB
    return tasks.scan(
        Select='ALL_ATTRIBUTES',
        ConsistentRead=True
    )['Items']


def delete_task(user_id, task_id):
    tasks.delete_item(
        Key={
            'user_id': user_id,
            'task_id': task_id
        }
    )


def get_all_user_tasks(user_id):
    response = tasks.query(
        KeyConditionExpression='user_id = :user_id',
        Select='ALL_ATTRIBUTES',
        ExpressionAttributeNames={
            ':user_id': user_id
        }
    )
    items = response['Items']
    print(items)
    return items


def get_phone_number(user_id):
    response = phone_numbers.get_item(Key={'user_id': user_id})
    if response.get('Item') is None:
        return None
    else:
        return response['Item']['number']


def set_phone_number(user_id, number):
    phone_numbers.put_item(
        Item={'user_id': user_id, 'number': number}
    )