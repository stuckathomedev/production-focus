from twilio.rest import Client
from db import get_all_tasks, get_phone_number
import algorithms
import datetime
import dateparser
from datetime import date
from ignore import account_id
from ignore import auth

client = Client(account_id, auth)


def send_completion(phone_number, completion, description):
    client.messages.create(to=phone_number,
                           from_="+16176827988",
                           body="Your current completion rate for your task of: '" + description + " is currently at:" + str(completion) + "% You may want to step it up or consider cancelling!")
    print("message sent!")


def due_within_hour(task):
    completed = dateparser.parse(task['last_completed']).date()
    days_since_completed = (date.today() - completed).days
    due_time_today = dateparser.parse(task['due_time'])
    time_within_hour = (due_time_today - datetime.datetime.now()).seconds <= 3600

    print(task, "due within hour:", time_within_hour, due_time_today, days_since_completed)

    if task['is_recurring']:
        if (days_since_completed % task['days_until'] == 0
                and time_within_hour):
            # It's either time to do it or a multiple of times to do it
            return True
        else:
            return False
    else:
        return days_since_completed == int(task['days_until']) and time_within_hour


def send_completion_reminders():
    results = [task for task in get_all_tasks() if due_within_hour(task)]

    for x in results:
        phone_number = get_phone_number(x['user_id'])
        if phone_number is None:
            print("No phone number; skip-u")
            continue
        due = due_within_hour(x)

        divergence = algorithms.calculate_divergence(x)
        print("Divergence:", divergence, "due within hour:", due)
        if divergence >= 0 and due:
            send_completion(phone_number, divergence, x['description'])
