import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Tasks')


def table_item_count():
    print(table.item_count)


def table_creation_time():
    print(table.creation_time)


def create_task(id, description, is_recurring, duration_interval, due_time, completions, trials, net_happiness, net_money):
    if trials > 0:
        completion_rate = completions / trials * 100
    else:
        completion_rate = 0

    table.put_item(
        Item={
            'CustomerID': id,
            'description': description,
            'is_recurring': is_recurring,
            'completed': False,
            'days_until': days_interval, # The number of days until the reminder triggers
            'due_time': due_time, # The specific time that the reminder should be triggered
            'completions': completions, # How many times one has completed the scheduled task
            'trials': trials, # The number of times that the task has executed
            'net_happiness': net_happiness, # Generated from DIVERGENCE
            'net_money': net_money, # Money based on happiness generation et al. Also gives features.
            'completion_rate': completion_rate, #Percentage per task
        }
    )


def search_intent(id):
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


def delete_intent(id):
    table.delete_item(
        Key={
            'CustomerID': id
        }
    )