from celery import Celery
from flask import Flask

# def make_celery(app):
#     celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
#                     broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#     class ContextTask(TaskBase):
#         abstract = True
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask
#     return celery
#
# flask_app = Flask(__name__)
# flask_app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )
# celery = make_celery(flask_app)
#
# # @celery.task()
# # def check_time():
# #     now = datetime.datetime.now()
# #     time = (now.strftime("%H:%M"))
# #     return time
#
# @celery.task()
# def add_together(a, b):
#     return a + b
#
# result = add_together.delay(23, 42)
# result.wait()

# app = Flask(__name__)
#
# @app.route('/')
# def hello_world():
#     now = datetime.datetime.now()
#     while True:
#         date = (now.strftime("%H:%M"))
#         return libj_date

from twilio.rest import Client
import datetime

account = "AC5324f49019d53ba87268a99cdb0fa482"
token = "87d3d6ffae6e6f81b9b2a6f5879c589e"
client = Client(account, token)


def send_message(dest_time):
    while True:
        now = datetime.datetime.now()
        time = (now.strftime("%H:%M"))
        print("It is not time yet")
        if time == dest_time:
            message = client.messages.create(to="9788448697",
                                             from_="+16176827988",
                                             body="This message will be sent at 5:00pm")
            print("message sent!")
            break;


send_message("17:03")