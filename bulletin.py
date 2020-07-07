# HammerBotPython
# bulletin.py

import discord


def exists(args, channel_history):
    exists_already = False
    for message in channel_history:
        if message.embeds:
            if message.embeds[0].title in " ".join(args):
                exists_already = True
                return exists_already

    return exists_already


def delete_bulletin(args, channel_history):
    project = " ".join(args)
    for message in channel_history:
        if message.embeds:
            if message.embeds[0].title == project:
                return message


def add_bulletin(project, formatted, channel_history):
    if project[:-1] == " ":
        project = project[:-1]
    for message in channel_history:
        if message.embeds:
            if message.embeds[0].title == project:
                edited_embed = discord.Embed(
                    color=0xe74c3c,
                    title=message.embeds[0].title,
                    description=message.embeds[0].description + "\n" + formatted
                )
                return message, edited_embed


def remove_bulletin(project, value_list, channel_history):
    for message in channel_history:
        if message.embeds:
            if message.embeds[0].title == project:
                bulletin_list = message.embeds[0].description.split("\n")
                for i in value_list:
                    for j in bulletin_list:
                        if i in j:
                            bulletin_list.remove(j)
                return bulletin_list, message
