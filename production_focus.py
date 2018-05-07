# coding=utf-8

# production_focus
# By Stuck@Home <h0m3stuck@gmail.com>
#
# An alexa skill to focus your production

import logging
from urllib.parse import urlparse
from datetime import datetime, date, timedelta
from uuid import uuid4

import dateparser
import phonenumbers
from flask import Flask, request as flask_request, render_template
from flask_ask import Ask, request, session, question, statement
import db
import algorithms
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
    return statement(render_template("no_nothing"))

@ask.intent('AMAZON.YesIntent')
def handle_yes():
    """
    (?) Handles the 'yes'  built-in intention.
    """
    return statement(render_template("yes_nothing"))


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
    return question(render_template("welcome"))


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
    print(search_string)
    #delete_words = stopwords.words('english')
    #terms = [word for word in search_string.split() if word not in delete_words]
    matching_tasks = [task for task in db.get_all_user_tasks(session.user.userId) if
                      search_string in task['description']]
    return matching_tasks


@ask.intent('CreateTodoIntent', convert={'due_date': 'date', 'due_time': 'time'})
def handle_create_todo(description, due_date, due_time):
    if description is None:
        return question(render_template("no_desc")).reprompt(render_template("reprompt"))
    if due_time is None:
        return question(render_template("no_due_time")).reprompt(render_template("reprompt"))
    if due_date is None:
        due_date = date.today()
    if due_date < date.today():
        return statement(render_template("time_travel_is_prohibited"))

    db.create_task(uuid4(), session.user.userId, description, False, (due_date - date.today()).days, due_time)

    created_text = render_template("created_todo",
                                   description=description,
                                   due_date=due_date,
                                   due_time=due_time)
    return statement(created_text)


@ask.intent('CreateReminderIntent', convert={'due_time': 'time'})
def handle_create_reminder(description, due_time):
    # this is terrible but it basically extracts the actual matched slot from Alexa
    # so "every two days" is converted into the canonical "every 2 days" slot as
    # described in the intent schema
    # if description is None or due_time is None:
    #     raise Exception("Required parameters have not been provided.")

    if description is None or due_time is None:
        return question(render_template("no_params"))

    try:
        repeat_interval = request["intent"]["slots"]["repeat_interval"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["name"]
    except:
        return statement(render_template("unknown_day_interval"))

    if repeat_interval == "every week":
        day_interval = 7
    elif repeat_interval == "every 3 days":
        day_interval = 3
    elif repeat_interval == "every 2 days":
        day_interval = 2
    elif repeat_interval == "every day":
        day_interval = 1
    else:
        # Subtly different from above try-except, because this means Alexa
        # successfully parsed a day interval, but *we* don't know what it is
        raise ValueError("Unknown day_interval received")

    db.create_task(uuid4(), session.user.userId, description, True, day_interval, due_time)
    created_text = render_template("created_reminder",
                                   description=description,
                                   repeat_interval=repeat_interval,
                                   due_time=due_time)
    return statement(created_text)


@ask.intent('ViewTasksIntent')
def handle_view_tasks():
    return statement(render_template("all_tasks", tasks=db.get_all_user_tasks(session.user.userId)))


@ask.intent('ViewDivergenceMeterIntent')
def handle_view_divergence_meter():
    user_tasks = db.get_all_user_tasks(session.user.userId)
    divergence = "{0:.6f}".format(algorithms.get_overall_divergence(user_tasks))
    uri = urlparse(flask_request.url)
    divergence_url = f"{uri.scheme}://{uri.netloc}/production/generate_nixie?pattern={divergence}"
    print("Got divergence: ", divergence)
    return statement(render_template("divergence_meter", meter=divergence))\
        .standard_card(title="Divergence Meter",
                       text=divergence,
                       small_image_url=divergence_url,
                       large_image_url=divergence_url)


@ask.intent('ViewHappinessIntent')
def handle_view_happiness():
    pass


@ask.intent('DeleteTaskIntent')
def handle_delete_task(description):
    if description is None:
        return question(render_template("no_desc"))\
            .reprompt(render_template("reprompt"))

    matches = search_for_task(description)
    descriptions = list(map(lambda task: task['description'], matches))
    if len(matches) == 0:
        return statement(render_template("no_matches"))
    if len(matches) > 1:
        if len(set(descriptions)) == 1:
            # All descriptions are identical; just delete them all
            for task in matches:
                db.delete_task(session.user.userId, task['task_id'])
            return statement(render_template("deleting_tasks", descriptions=descriptions))
        else:
            return statement(render_template("more_than_one_match",
                                         num=len(matches),
                                         descriptions=str([match['description'] for match in matches])))
    else:
        match = matches[0]
        db.delete_task(session.user.userId, match['task_id'])
        return statement(render_template("deleting_task", description=match['description']))


@ask.intent('ViewMailboxIntent')
def handle_view_mailbox():
    pass


def reminder_doable_today(task):
    if task['is_recurring'] == True:
        next_due_on = dateparser.parse(task['last_completed']).date() + timedelta(days=int(task['days_until']))
        return next_due_on == date.today()
    else:
        return True  # lel


@ask.intent('CompleteTaskIntent')
def handle_complete_task(description):
    if description is None:
        return question(render_template("no_desc"))\
            .reprompt(render_template("reprompt"))

    # Only get undone tasks matching the description
    matches = search_for_task(description)
    if len(matches) == 0:
        return statement(render_template("no_matches"))
    if len(matches) > 1:
        return statement(render_template("more_than_one_match",
                                         num=len(matches),
                                         descriptions=str([match['description'] for match in matches])))
    match = matches[0]
    if match['completed'] == True:
        return statement(render_template("todo_already_done"))
    if reminder_doable_today(match) == False:
        return statement(render_template("reminder_not_yet_due"))

    task_divergence = algorithms.calculate_divergence(match)
    overall_divergence = algorithms.get_overall_divergence(db.get_all_user_tasks(session.user.userId))

    db.update_task(session.user.userId, match['task_id'], completions=match['completions'] + 1)
    if match['is_recurring'] == True:
        # Calculate # of trials missed
        last_completed = dateparser.parse(match['last_completed']).date()
        today = date.today()
        days_until = timedelta(days=int(match['days_until']))

        # Calculates # of trials - get # of days since last completed,
        # floordiv by day interval, subtract one to get *missed* trials
        # not counting this one
        trials_missed = min(0, (today - last_completed) // days_until - 1)

        db.update_task(session.user.userId, match['task_id'],
                       last_completed=str(date.today()),
                       trials=match['trials'] + trials_missed + 1,
                       completions=match['completions'] + 1)
        return statement(render_template("completed_reminder",
                                         description=match['description'],
                                         days_until=days_until.days,
                                         task_divergence=task_divergence,
                                         overall_divergence=overall_divergence))
    else:
        # Not recurring, simply mark as done
        db.update_task(session.user.userId, match['task_id'],
                       last_completed=str(date.today()),
                       completed=True,
                       completions=1,
                       trials=1)
        return statement(render_template("completed_todo",
                                         description=match['description'],
                                         task_divergence=task_divergence,
                                         overall_divergence=overall_divergence))


def is_valid_phone_number(number: str):
    try:
        possible = phonenumbers.parse(number, "US")
        return phonenumbers.is_valid_number(possible)
    except phonenumbers.NumberParseException:
        return False


@ask.intent('SetPhoneNumberIntent')
def handle_set_phone_number(number):
    if not is_valid_phone_number(number):
        return question(render_template("invalid_number")).reprompt(render_template("reprompt"))

    db.set_phone_number(session.user.userId, number)
    return statement(render_template("set_phone_number", number=number))


if __name__ == '__main__':
    app.run(debug=True)