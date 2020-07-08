# HammerBotPython
# bulletin.py

import discord
from utils import format_conversion


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


async def task_list(ctx, action, use, args="",):
    if use == "bulletin":
        channel_history = await ctx.channel.history(limit=50).flatten()
    elif use == "todo":
        channel_history = await ctx.channel.pins()
    else:
        return

    if not args:
        response = "I'm sorry but you didn't specify anything."
        await ctx.send(response, delete_after=5)
        return

    exists_already = exists(args, channel_history)

    if action == "delete":
        await delete_bulletin(args, channel_history).delete()
        return

    formatted, project, value_list = format_conversion(args, "bulletin")

    if not project:
        response = "I'm sorry but you didn't specify a project"
        await ctx.send(response, delete_after=5)
        return

    if not value_list:
        response = "I'm sorry but you didn't specify any tasks"
        await ctx.send(response, delete_after=5)
        return

    if action == "create":
        if exists_already:
            response = "I'm sorry but this board already exists"
            await ctx.send(response, delete_after=5)
            return

        embed = discord.Embed(
            color=0xe74c3c,
            title=project,
            description=formatted
        )
        task = await ctx.send(embed=embed)
        if use == "todo":
            await task.pin()
            return
        return

    if not exists_already:
        response = "I'm sorry but this board doesn't exist"
        await ctx.send(response, delete_after=5)
        return

    if action == "add":
        message, embed = add_bulletin(project, formatted, channel_history)
        await message.edit(embed=embed)
        return

    if action == "remove":
        bulletin_list, message = remove_bulletin(project, value_list, channel_history)
        if bulletin_list:
            edited_embed = discord.Embed(
                color=0xe74c3c,
                title=message.embeds[0].title,
                description="\n".join(bulletin_list))
            await message.edit(embed=edited_embed)
            return

        else:
            await message.delete()
            return
