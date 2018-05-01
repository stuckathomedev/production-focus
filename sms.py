from twilio.rest import Client
from db import get_all_tasks, get_phone_number
import algorithms
import dateparser
from datetime import date, datetime
from ignore import account_id
from ignore import auth

client = Client(account_id, auth)


def send_completion(phone_number, divergence, task_description):
    body = (f"Remember to do your task of '{task_description}'! " +
            "Your current divergence rate is at {str(divergence)}%. " +
            "You may want to either step it up or consider cancelling this task!\n\n" +
            "Sincerely, you from the future (via Production Focus)")

    client.messages.create(to=phone_number,
                           from_="+16176827988",
                           body=body)
    print("message sent!")


def due_within_hour(task):
    completed = dateparser.parse(task['last_completed']).date()
    days_since_completed = (date.today() - completed).days
    due_time_today = dateparser.parse(task['due_time'])
    time_within_hour = (due_time_today - datetime.now()).seconds <= 3600

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
    for task in get_all_tasks():
        try:
            if not due_within_hour(task):
                print("Not sending SMS for task, as it's not due in the next hour")
                print("Current time:", datetime.now())
                continue

            phone_number = get_phone_number(task['user_id'])
            if phone_number is None:
                print("No phone number; skip-u")
                continue

            divergence = algorithms.calculate_divergence(task)
            if divergence > 0.2:
                print("Not sending SMS for task, as divergence is too low")
                print("Divergence:", divergence)
                continue

            print("Divergence:", divergence)
            print("Phone number:", phone_number)
            print("Sending SMS")
            send_completion(phone_number, divergence, task['description'])
        except Exception as e:
            print("Hmm hit exception while processing task, fixme?", e)
