from twilio.rest import Client
from db import get_all_tasks, get_phone_number
import algorithms
import datetime
from datetime import date, time, timedelta
import threading

account = "AC5324f49019d53ba87268a99cdb0fa482"
token = "87d3d6ffae6e6f81b9b2a6f5879c589e"
client = Client(account, token)


def send_message(dest_time, mensaje):
    while True:
        now = datetime.datetime.now()
        time_current = (now.strftime("%H:%M"))
        if time_current == dest_time:
            message = client.messages.create(to="9788448697",
                                             from_="+16176827988",
                                             body=mensaje)
            print("message sent!")
            break


def send_completion(phone_number, completion, description):
    client.messages.create(to=phone_number,
                           from_="+16176827988",
                           body="Your current completion rate for your task of: '" + description + " is currently at:" + completion + "% You may want to step it up or consider cancelling!")
    print("message sent!")


def send_message_thread(time, message):
    t = threading.Thread(target=send_message, args=(time, message))
    t.start()


def send_message_completion(time, completion, description):
    t = threading.Thread(target=send_completion, args=(time, completion, description))
    t.start()


def due_within_hour(task):
    completed = date(task['last_completed'])
    days_since_completed = (date.today() - completed).days
    time_within_hour = (datetime.datetime.now() - datetime.datetime.combine(date.today(), task['due_time'])).seconds <= 3600

    if task['is_recurring'] == True:
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