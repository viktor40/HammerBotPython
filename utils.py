# HammerBotPython
# utils.py

import discord
from data import discord_letters


def format_conversion(args, command):
    value_list = []
    description = ""
    value = ""
    for i in args:
        if "|" in i:
            value += i[:-1]
            description = value[:-1]
            value = ""
        elif "&" not in i:
            value += i + " "
        else:
            value += i
            value_list.append(value[:-1])
            value = ""

    value_list.append(value[:-1])
    formatted = ""
    if command == "poll":
        for pos, option in enumerate(value_list):
            formatted += discord_letters[pos] + " " + option + "\n"
        return formatted, value_list, description
    elif command == "bulletin":
        for pos, option in enumerate(value_list):
            formatted += "- " + option + "\n"
        return formatted, description, value_list


def get_server_roles(ctx):
    roles = ctx.guild.roles
    role_list = [i.name for i in roles]
    return role_list
