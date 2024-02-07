from dotenv import load_dotenv
from flask import request

from app import create_app
from app.core.processing import Processing
from app.api.slack.message_templates import bot_messages
from app.api.slack.operations import send_message
from app.api.slack.views.app_home_opened import app_home_opened

load_dotenv()
app, slack_app, handler = create_app()
processing = Processing()


@app.route("/56a6b448-321k-8855-ha2qe-pa231qrt1/chatbot/slack/events", methods=["POST"])
def slack_events():
    """
    Handles incoming Slack events using the Bolt's request handler

    """
    return handler.handle(request)


@app.route('/chatbot', methods=['GET'])
def chatbot_home():
    return "Welcome chatbot Api"


@slack_app.event("app_home_opened")
def update_home_tab(client, event, logger):
    """
     Updates the app home tab with a specific view
     param str client: The Slack SDK WebClient instance
     param str event: The event data
     param str logger: The logger instance

    """
    try:
        client.views_publish(
            user_id=event["user"],
            view=app_home_opened
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@slack_app.event("app_mention")
def app_mention(body, ack, say):
    """
     Handles app mention events and responds accordingly
     param str body: The event body
     param str ack: The acknowledgment function
     param str say: The say function for sending a message

    """
    ack()
    event_type = body["event"]["type"]
    data = body["event"]["text"]

    if event_type == "app_mention":
        if "process" in data:
            message = "Hello! My name is Chatbot. Wait a moment, We are processing the transaction..."
            user = body["event"]["user"]
            channel = body["event"]["channel"]
            handle_processing_mention(channel, message, user)
        elif "test" in data:
            handle_test_mention(say)
        elif "static winner" in data:
            channel = body["event"]["channel"]
            handle_static_winner_mention(channel)
        elif "dynamic winner" in data:
            contestants = body["event"]["text"].split(" ")[3]
            channel = body["event"]["channel"]
            handle_dynamic_winner_mention(channel, contestants.split(","))
        elif "enter information winner name" in data:
            contestant = body["event"]["text"].split(" ")[5]
            channel = body["event"]["channel"]
            handle_winner_mention(channel, contestant)


def handle_processing_mention(channel, message, user):
    """
    Handles the "processing" mention and sends a welcome message
    param str channel: The Slack channel ID
    param str message: The message to include in the welcome message
    param str user: The user information

    """
    send_message(channel, bot_messages["welcome_message"].format(
        project=user, task_id=message))


def handle_static_winner_mention(channel):
    """
    Handles the "winner" mention and sends a welcome message
    param str channel: The Slack channel ID
    param str message: The message to include in the welcome message
    param str user: The user information

    """
    winner_users = processing.get_random_people()
    message = "Static Winner User : "
    for winner_user in winner_users:
        message += "`" + winner_user + "` "
    send_message(channel, message)


def handle_dynamic_winner_mention(channel, contestants):
    """
    Handles the "dynamic winner" mention and sends a welcome message
    param str channel: The Slack channel ID
    param str message: The message to include in the welcome message
    param str user: The user information

    """
    winner_users = processing.get_random_people(contestants=contestants)
    message = "Dynamic Winner User : "
    for winner_user in winner_users:
        message += "`" + winner_user + "` "
    send_message(channel, message)


def handle_test_mention(say):
    """
    Handles the "test" mention and sends a testing message.
    param str say: The say function for sending a message.

    """
    say("Testing...")


@slack_app.action("winner-button-action")
def handle_winner_information_button_click(ack, body, client):
    """
    :param ack: slack response handler
    :param body: request body
    :param client: slack client

    """
    ack()
    channel_id = body["channel"]["id"]
    message_ts = body["container"]["message_ts"]
    winner_name = body["actions"][0]["value"].split("::")[1]
    client.views_open(
        trigger_id=body["trigger_id"],
        view=processing.winner_contestants_modal(winner_name, channel_id, message_ts))


def handle_winner_mention(channel_name, winner_name):
    send_message(
        channel_id=channel_name,
        message="",
        blocks=processing.enter_winner_information_button(winner_contestants=winner_name)['blocks']
    )

@slack_app.view_submission('winner_contestants_modal')
def handle_modal_submission(ack, body, view, client):
    ack()
    values = view['private_metadata'].split("::")
    winner_contestants = values[0]
    channel_id = values[1]
    message_ts = values[2]
    starter_block = processing.winner_contestants_starter_button_response(winner_contestants)['blocks']
    client.chat_update(channel=channel_id, ts=message_ts, blocks=starter_block)
    client.chat_postMessage(channel=body['user']['id'], text="Thank you for your submission! :white_heart:")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
