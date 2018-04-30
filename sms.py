from twilio.rest import Client
from db import get_all_tasks, get_phone_number
import algorithms
import datetime
import dateparser
from datetime import date

account = "AC5324f49019d53ba87268a99cdb0fa482"
token = "87d3d6ffae6e6f81b9b2a6f5879c589e"
client = Client(account, token)


def send_completion(phone_number, completion, description):
    client.messages.create(to=phone_number,
                           from_="+16176827988",
                           body="Your current completion rate for your task of: '" + description + " is currently at:" + completion + "% You may want to step it up or consider cancelling!")
    print("message sent!")


def due_within_hour(task):
    completed = dateparser.parse(task['last_completed']).date()
    days_since_completed = (date.today() - completed).days
    time_within_hour = (datetime.datetime.now() -
                        datetime.datetime.combine(date.today(),
                                                  dateparser.parse(task['due_time']).time())).seconds <= 3600

    print(task, "due within hour:", time_within_hour)

    if task['is_recurring']:
        if (days_since_completed % task['days_until'] == 0
                and time_within_hour):
            # It's either time to do it or a multiple of times to do it
            return True
        else:
            return False
    else:
        return days_since_completed == task['days_until'] and time_within_hour


def send_completion_reminders():
    results = [task for task in get_all_tasks() if due_within_hour(task)]

    for x in results:
        phone_number = get_phone_number(x['user_id'])
        if phone_number is None:
            continue

        divergence = algorithms.calculate_divergence(x)
        if divergence > 50 and due_within_hour(x):
            send_completion(phone_number, divergence, x['description'])
