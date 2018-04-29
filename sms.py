from twilio.rest import Client
from db import search_by_user
import datetime
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
            break;


def send_completion(dest_time, completion, description):
    while True:
        now = datetime.datetime.now()
        time_current = (now.strftime("%H:%M"))
        if time_current == dest_time:
            message = client.messages.create(to="9788448697",
                                             from_="+16176827988",
                                             body="Your current completion rate for your intent of: '" + description + " is currently at:" + completion + "% You may want to step it up or consider cancelling!")
            print("message sent!")
            break;


def send_message_thread(time, message):
    t = threading.Thread(target=send_message, args=(time, message))
    t.start()


def send_message_completion(time, completion, description):
    t = threading.Thread(target=send_completion, args=(time, completion, description))
    t.start()


def send_completion_reminders(user_id, time):
    user_results = search_by_user(user_id)
    for x in user_results:
        completions = x[completions]
        trials = x[trials]
        description = x[description]
        divergance = (completions / trials)*100
        if divergance > 50:
            send_message_completion(time, divergance, description)
        else:
            continue
    return 0
