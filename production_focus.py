# coding=utf-8

# production_focus
# By Stuck@Home <h0m3stuck@gmail.com>
#
# An alexa skill to focus your production

import logging
from datetime import datetime, date
from uuid import uuid4

from nltk.corpus import stopwords
from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement
import db
from routes import routes

__author__ = 'Stuck@Home'
__email__ = 'h0m3stuck@gmail.com'


app = Flask(__name__)
app.register_blueprint(routes)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Session starter
#
# This intent is fired automatically at the point of launch (= when the session starts).
# Use it to register a state machine for things you want to keep track of, such as what the last intent was, so as to be
# able to give contextual help.

@ask.on_session_started
def start_session():
    """
    Fired at the start of the session, this is a great place to initialise state variables and the like.
    """
    logging.debug("Session started at {}".format(datetime.now().isoformat()))

# Launch intent
#
# This intent is fired automatically at the point of launch.
# Use it as a way to introduce your Skill and say hello to the user. If you envisage your Skill to work using the
# one-shot paradigm (i.e. the invocation statement contains all the parameters that are required for returning the
# result

@ask.launch
def handle_launch():
    """
    (QUESTION) Responds to the launch of the Skill with a welcome statement and a card.

    Templates:
    * Initial statement: 'welcome'
    * Reprompt statement: 'welcome_re'
    * Card title: 'production_focus
    * Card body: 'welcome_card'
    """

    welcome_text = render_template('welcome')
    welcome_re_text = render_template('welcome_re')
    welcome_card_text = render_template('welcome_card')

    return question(welcome_text).reprompt(welcome_re_text).standard_card(title="production_focus",
                                                                          text=welcome_card_text)


# Built-in intents
#
# These intents are built-in intents. Conveniently, built-in intents do not need you to define utterances, so you can
# use them straight out of the box. Depending on whether you wish to implement these in your application, you may keep
# or delete them/comment them out.
#
# More about built-in intents: http://d.pr/KKyx

@ask.intent('AMAZON.StopIntent')
def handle_stop():
    """
    (STATEMENT) Handles the 'stop' built-in intention.
    """
    farewell_text = render_template('stop_bye')
    return statement(farewell_text)


@ask.intent('AMAZON.CancelIntent')
def handle_cancel():
    """
    (STATEMENT) Handles the 'cancel' built-in intention.
    """
    farewell_text = render_template('cancel_bye')
    return statement(farewell_text)


@ask.intent('AMAZON.HelpIntent')
def handle_help():
    """
    (QUESTION) Handles the 'help' built-in intention.

    You can provide context-specific help here by rendering templates conditional on the help referrer.
    """

    help_text = render_template('help_text')
    return question(help_text)


@ask.intent('AMAZON.NoIntent')
def handle_no():
    """
    (?) Handles the 'no' built-in intention.
    """
    pass

@ask.intent('AMAZON.YesIntent')
def handle_yes():
    """
    (?) Handles the 'yes'  built-in intention.
    """
    pass


@ask.intent('AMAZON.PreviousIntent')
def handle_back():
    """
    (?) Handles the 'go back!'  built-in intention.
    """
    pass

@ask.intent('AMAZON.StartOverIntent')
def start_over():
    """
    (QUESTION) Handles the 'start over!'  built-in intention.
    """
    pass


# Ending session
#
# This intention ends the session.

@ask.session_ended
def session_ended():
    """
    Returns an empty for `session_ended`.

    .. warning::

    The status of this is somewhat controversial. The `official documentation`_ states that you cannot return a response
    to ``SessionEndedRequest``. However, if it only returns a ``200/OK``, the quit utterance (which is a default test
    utterance!) will return an error and the skill will not validate.

    """
    return statement("")


def search_for_task(search_string):
    #delete_words = stopwords.words('english')
    #terms = [word for word in search_string.split() if word not in delete_words]
    #matching_tasks = [task for task in tasks if
    #                  all(term for term in terms if task.description.find(term) != 1)]
    #return matching_tasks
    pass


def get_divergence_meter() -> float:
    #divergence = completions / trials
    #return divergence
    pass


@ask.intent('CreateTodoIntent', convert={'due_date': 'date', 'due_time': 'time'})
def handle_create_todo(description, due_date, due_time):
    if due_date is None:
        due_date = date.today()

    db.create_task(uuid4(), description, False, due_date() )

    created_text = render_template("created_todo", description=description, due_date=due_date, due_time=due_time)
    # todo upload to dynamodb
    return statement(created_text)


@ask.intent('CreateReminderIntent', convert={'due_time': 'time'})
def handle_create_reminder(description, repeat_interval, due_time):
    # this is terrible but it basically extracts the actual matched slot from Alexa
    # so "every two days" is converted into the canonical "every 2 days" slot as
    # described in the intent schema

    repeat_interval = request["intent"]["slots"]["repeat_interval"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["name"]

    db.create_task(uuid4(), description, True, repeat_interval, 0, 0, 0, 0)
    created_text = render_template("created_reminder",
                                   description=description,
                                   repeat_interval=repeat_interval,
                                   due_time=due_time)
    return statement(created_text)


@ask.intent('ViewTasksIntent')
def handle_view_tasks():
    pass


@ask.intent('ViewDivergenceMeterIntent')
def handle_view_divergence_meter():
    return statement(render_template("divergence_meter", meter="0.00"))\
        .standard_card(title="Divergence Meter",
                       text="0.00",
                       small_image_url="https://production-focus2.localtunnel.me/generate_nixie?pattern=0.337187",
                       large_image_url="https://production-focus2.localtunnel.me/generate_nixie?pattern=0.337187")


@ask.intent('ViewHappinessIntent')
def handle_view_happiness():
    pass


@ask.intent('DeleteTaskIntent')
def handle_delete_task(description):
    matches = search_for_task(description)
    if len(matches) == 0:
        return statement(render_template("no_matches"))
    if len(matches) > 1:
        return statement(render_template("more_than_one_match",
                                         num=len(matches),
                                         descriptions=str([match.description for match in matches])))

    match = matches[0]
    return statement(render_template("deleting_task", description=match.description))


@ask.intent('ViewMailboxIntent')
def handle_view_mailbox():
    pass


@ask.intent('CompleteTaskIntent')
def handle_complete_task(description):
    matches = search_for_task(description)
    if len(matches) == 0:
        return statement(render_template("no_matches"))
    if len(matches) > 1:
        return statement(render_template("more_than_one_match",
                                         num=len(matches),
                                         descriptions=str([match.description for match in matches])))

    match = matches[0]
    return statement(render_template("completed_task", description=match.description, meter=get_divergence_meter()))


if __name__ == '__main__':
    app.run(debug=True)
