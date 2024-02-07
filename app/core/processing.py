import logging
import random

from app.core.constants import team_member

logger = logging.getLogger(__name__)


class Processing:
    """Class for processing and includes business logics"""

    def get_random_people(self, contestants=team_member):
        """

        :return:
        """
        selected_names = random.sample(contestants, 2)
        return selected_names

    def enter_winner_information_button(self, winner_contestants):
        """
        :param winner_contestants: winner_contestants

        """
        return {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Welcome <@{winner_contestants}> to the Winner Contestants."
                                f" Please share your information with us so we can reach you"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Share",
                            "emoji": True
                        },
                        "value": "winner_information" + "::" + winner_contestants,
                        "action_id": "winner-button-action"
                    }
                }
            ]
        }

    def winner_contestants_modal(self, winner_contestants, channel_id, message_ts):
        return {
            "type": "modal",
            "callback_id": "winner_contestants_modal",
            "private_metadata": f"{winner_contestants}::{channel_id}::{message_ts}",
            "title": {
                "type": "plain_text",
                "text": "Winner Form",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [
                                {
                                    "type": "text",
                                    "text": f"Hello {winner_contestants} this is Winner Information form. \n"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "input",
                    "element": {
                        "type": "number_input",
                        "is_decimal_allowed": False,
                        "action_id": "number_input-action",
                        "min_value": "0",
                        "max_value": "99999999999"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Phone Number: (Max 11 char)",
                        "emoji": True
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "image",
                            "image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
                            "alt_text": "cute cat"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*(Max 11 char)* "
                        }
                    ]
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Name & Surname",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Email",
                        "emoji": True
                    }
                }
            ]
        }

    def winner_contestants_starter_button_response(self, winner_contestants):
        """
        Message to be sent to the user when the contestants started with app mention response
        :return: block message

        """
        return {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Your winner contestants information data {winner_contestants} sent!"
                    }
                }
            ]
        }