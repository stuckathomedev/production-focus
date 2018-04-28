from twilio.rest import Client
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


def send_divergance(dest_time, divergance):
    while True:
        now = datetime.datetime.now()
        time_current = (now.strftime("%H:%M"))
        if time_current == dest_time:
            message = client.messages.create(to="9788448697",
                                             from_="+16176827988",
                                             body="Your current divergence is: " + divergance + "!")
            print("message sent!")
            break;


def send_message_thread(time, message):
    t = threading.Thread(target=send_message, args=(time, message))
    t.start()


def send_message_divergance(time, divergance):
    t = threading.Thread(target=send_divergance, args=(time, divergance))
    t.start()