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
from discord.ext.commands.context import Context

from utilities.data import discord_letters


# Convert something from the format <> | <> & <> & <> ... in the correct way to variables for easy usage.
def format_conversion(args):
    arg_string = ' '.join(args)
    if '|' in arg_string:
        title, options = arg_string.split('|')
        options = options.split('&')
        title = strip_surrounding(title)
        options = [strip_surrounding(option) for option in options]
    else:
        title, options = arg_string, None
    return title, options


def strip_surrounding(word):
    if word[0] == ' ':
        word = word[1:]
    if word[-1] == ' ':
        word = word[:-1]
    return word


# get a list of all roles in the server
def get_server_roles(ctx):
    roles = ctx.guild.roles
    role_list = [i.name for i in roles]
    return role_list


def time_test(input_func):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = input_func(*args, **kwargs)
        end_time = time.time()
        print("Method Name - {0}, Args - {1}, Kwargs - {2}, Execution Time - {3}".format(input_func.__name__, args, kwargs, end_time - start_time))
        return result
    return timed


def disable_for_debug(input_func):
    """
    A method to disable a function when debug mode is enabled.
    Whenever a method has this decorator, it will be d

    :param input_func: The function to disable.
    :return:
    """
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, Context) and arg.bot.debug:
                return input_func(*args)
            else:
                return
    return wrapper
