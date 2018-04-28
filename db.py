import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Tasks')


def table_item_count():
    print(table.item_count)


def table_creation_time():
    print(table.creation_date_time)


def create_task(id, title, contents, is_recurring, task_status, date, completions, trials, net_happiness, net_money):
    if trials > 0:
        completion_rate = completions/trials*100
    else:
        completion_rate = 0

    table.put_item(
        Item={
            'CustomerID': id,
            'title': title,
            'contents': contents,
            'is_recurring': is_recurring,
            'status': task_status,
            'date': date,
            'completions': completions,
            'trials': trials,
            'net_happiness': net_happiness,
            'net_money': net_money,
            'completion_rate': completion_rate,
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