from os import environ

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse

token = environ.get('SLACK_BOT_TOKEN')
signing_secret = environ.get('SLACK_SIGNING_SECRET')
client = WebClient(token=token)


def send_message(channel_id: str, message=None, attachments=None, thread_ts=None, blocks=None, icon_url=None,
                 user_name="chatbot", unfurl_links=None) -> SlackResponse:
    """
    Sends a message to a specified Slack channel using the Slack API `chat_postMessage` method and
    Returns a dictionary representing the Slack API response
    param str channel_id: A string representing the ID of the Slack channel where the message will be sent.
    param str message: A string representing the text message to be sent.
    param dict attachments: A dictionary representing optional attachments to be included in the message.
    param dict block: A dictionary representing optional blocks to be included in the message.
    param bool unfurl_links: A boolean representing whether links should be unfurled in the message.

    """
    return client.chat_postMessage(
        channel=channel_id,
        text=message,
        blocks=blocks,
        attachments=attachments,
        username=user_name,
        thread_ts=thread_ts,
        icon_url=icon_url,
        unfurl_links=unfurl_links,
        as_user=True
    )


def update_message(channel_id: str, message: str, ts: str, attachments=None) -> dict:
    """
    Updates an existing message in a specified Slack channel using the Slack API `chat_update` method and
    Returns a dictionary representing the Slack API response.
    param str channel_id: A string representing the ID of the Slack channel where the message to be updated exists.
    param str message: A string representing the updated text message.
    param str ts: A string representing the timestamp of the message to be updated.
    param dict  attachments: A dictionary representing optional attachments to be included in the updated message.

    """
    return client.chat_update(
        channel=channel_id,
        text=message,
        ts=ts,
        attachments=attachments,
        as_user=True
    )

