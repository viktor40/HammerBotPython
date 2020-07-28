# HammerBotPython
# coordinates.py

from utilities.data import hammer_bot_id


"""
Left over code from older versions. Will most likely be deleted soon and is not used.
"""

def edit(message, channel_history):
    # add the new message to the old message
    coordinate_message = channel_history[0]
    coordinate_list = coordinate_message.content
    return coordinate_list + "\n" + message.content


def create_new_message(channel_history):
    character_limit = 2000
    return not channel_history or len(channel_history[0].content) >= character_limit


def delete(coordinate, channel_history):
    for message in channel_history:
        if message.author.id == hammer_bot_id:
            if coordinate in message.content.split("\n"):
                coordinate_list = message.content.split("\n")
                coordinate_list.remove(coordinate)
                return message, "\n".join(coordinate_list)


def in_message(coordinate, channel_history):
    for message in channel_history:
        if message.author.id == hammer_bot_id:
            for coord in message.content.split("\n"):
                if coord == coordinate:
                    return True
    return False


def check_format(message):
    try:
        message_format = message.content.split()
        correct_prefix = message_format[0].startswith("ow_") or message_format[0].startswith("n_")
        has_colon = (message_format[0][-1] == ":")
        has_coordinates = message_format[1].isnumeric and message_format[2].isnumeric and message_format[3].isnumeric
        return correct_prefix and has_colon and has_coordinates

    except IndexError:
        return False
