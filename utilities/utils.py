# HammerBotPython
# utilities module
# utils.py

"""
utils.py holds some utilities which can be used in various places.
format_conversion will convert the format we use in discord to something we can easily work with in python.
get_server_roles will get all roles available on the server.
timetest can be used as a decorator to test the speed of a certain method.
"""

import time

from utilities.data import discord_letters


# Convert something from the format <> | <> & <> & <> ... in the correct way to variables for easy usage.
def format_conversion(args, command):
    value_list = []
    description = ""
    value = ""
    for i in args:
        # everything before | is the description
        if "|" in i:
            value += i[:-1]
            description = value[:-1]
            value = ""

        # everything after | are options split by &
        elif "&" not in i:
            value += i + " "
        else:
            value += i
            value_list.append(value[:-1])
            value = ""

    value_list.append(value[:-1])
    formatted = ""

    # For polls we add a emote letter in front instead of a dash which is used for bulletins and others.
    if command == "poll":
        for pos, option in enumerate(value_list):
            formatted += discord_letters[pos] + " " + option + "\n"
        return formatted, value_list, description
    elif command == "bulletin":
        for pos, option in enumerate(value_list):
            formatted += "- " + option + "\n"
        return formatted, description, value_list


# get a list of all roles in the server
def get_server_roles(ctx):
    roles = ctx.guild.roles
    role_list = [i.name for i in roles]
    return role_list


def tim_etest(input_func):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = input_func(*args, **kwargs)
        end_time = time.time()
        print("Method Name - {0}, Args - {1}, Kwargs - {2}, Execution Time - {3}".format(input_func.__name__, args, kwargs, end_time - start_time))
        return result
    return timed
