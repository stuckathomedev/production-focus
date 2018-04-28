import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('Tasks')


def table_item_count():
    print(table.item_count)


def table_creation_time():
    print(table.creation_date_time)


def create_task(CustomerID, title, contents, is_recurring, task_status, date, completions, trials, net_happiness, net_money):
    if trials > 0:
        completion_rate = completions/trials*100
    else:
        completion_rate = 0

    table.put_item(
        Item={
            'CustomerID': CustomerID,
            'title': title,
            'contents': contents,
            'isRecurring': is_recurring,
            'status': task_status,
            'date': date,
            'completions': completions,
            'trials': trials,
            'net-happiness': net_happiness,
            'net-money': net_money,
            'completion-rate': completion_rate,
        }
    )


def search_intent(CustomerID):
    response = table.get_item(
        Key={
            'CustomerID': CustomerID
        }
    )
    item = response['Item']
    print(item)


def update_intent(CustomerID, **kwargs):
    for key, value in kwargs.items():
        table.update_item(
            Key={
                'CustomerID': CustomerID
            },
            UpdateExpression=f'SET {key} = :vary',
            ExpressionAttributeValues={
                ':vary': value
            }
        )


def delete_intent(CustomerID):
    table.delete_item(
        Key={
            'CustomerID': CustomerID
        }
    )