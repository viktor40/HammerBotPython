# HammerBotPython
# utilities module
# utils.py

"""
utils.py holds some utilities which can be used in various places.
    - format_conversion: Implementation of a conversion to a more usable format of the <> | <> & <> & ... format
                         the bot uses in various commands to make it more human usable.
    - get_server_roles: A wrapper for Guilds.roles to return a list of strings containing role names instead
                        of a list of Role objects.
    - time_test: A decorator that can be used to test how fast a method executes
    - disable_for_debug: A decorator that is used to disable functions in debug mode.
"""

import time
from discord.ext.commands.context import Context
from discord.ext.commands.bot import Bot

from utilities.data import discord_letters


def format_conversion(args):
    """
    Convert something from the format <> | <> & <> & <> ... in the correct way to variables for easy usage.
    We check if | is in args so the method can be used more generally.

    :param args: Something formatted like: <> | <> & <> & <> ...
    :return: title: The title of the formatted string (Everything in front of |)
    :return: options: A list containing all options (after |, between the &)
    """
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
    """
    Strip spaces in the front or back of word.

    :param word: A word (or sentence) of which we want to strip the surrounding spaces.
    :return: A string that doesn't start or end with a space.
    """
    while word and (word[0] != ' ' or word[-1] != ' '):
        if word[0] == ' ':
            word = word[1:]
        if word[-1] == ' ':
            word = word[:-1]
    return word


def get_server_roles(ctx):
    """
    Convert the Guild.roles list containing Role objects to a list containing strings which represent the role name.

    :param ctx: a discord.ext.commands.context.Context object containing the bot's context
    :return: a list containing strings ([Role.name])
    """
    roles = ctx.guild.roles
    role_list = [i.name for i in roles]
    return role_list


def time_test(input_func):
    """
    A method used to test the performance of a method.

    :param input_func: The function of which we want to test the perfomrance.
    """
    def timed(*args, **kwargs):
        start_time = time.time()
        result = input_func(*args, **kwargs)
        end_time = time.time()
        print("Method Name - {0}, Args - {1}, Kwargs - {2}, Execution Time - {3}".format(input_func.__name__,
                                                                                         args,
                                                                                         kwargs,
                                                                                         end_time - start_time))
        return result
    return timed


class ForbiddenChessMove(Exception):
    """Exception raised when using a forbidden chess move.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="This is not a valid chess move!"):
        self.message = message
        super().__init__(self.message)


def disable_for_debug(func):
    """
    A method to disable a function when debug mode is enabled.
    Whenever a method has this decorator, it will be disabled, provided a context or bot argument is passed
    to the function.

    :param func: The function to disable.
    """
    def wrapper(*args, **kwargs):
        for arg in args:

            if isinstance(arg, Context):
                if arg.bot.debug:
                    return
                else:
                    return func(*args)

            elif isinstance(arg, Bot):
                if arg.debug:
                    return
                else:
                    return func(*args)

        print('Not disabling function {}. This method does not have a context'.format(func.__name__))
        return func(*args)
    return wrapper
