# HammerBotPython
# other module
# task.py

"""
task.py will handle different task embeds such as the coordinate embeds, the bulletin board and the to do embeds.
This embed allows everyone to add or remove things from the embed, which isn't possible with user sent messages.
Furthermore it will do automatic formatting and everyone will be able to delete the embeds.
"""

import discord
from discord.ext import commands

from utilities.utils import format_conversion
import cogs.help_command.help_data as hd
import utilities.data as data


class TaskCommand(commands.Cog):
    """
    This cog is used to implement the bulletin, to-do and coordinate command.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
    """

    def __init__(self, bot):
        self.bot = bot

    # Command to create, add, remove and delete bulletins in the bulletin board.
    @commands.command(name='bulletin', help=hd.bulletin_help, usage=hd.bulletin_usage)
    @commands.has_role(data.member_role_id)
    async def bulletin(self, ctx, action, *args):
        await ctx.message.delete()
        await task_list(ctx=ctx, action=action, args=args, use='bulletin')

    # Command to add a to do list to a project channel and pin it.
    @commands.command(name='todo', help=hd.todo_help, usage=hd.todo_usage)
    @commands.has_role(data.member_role_id)
    async def todo(self, ctx, action, *args):
        await ctx.message.delete()
        await task_list(ctx=ctx, action=action, args=args, use='todo')

    # Command to handle the coordinate list. There is one embed per dimension
    @commands.command(name='coordinates', help=hd.coordinates_help, usage=hd.coordinates_usage)
    @commands.has_role(data.member_role_id)
    async def coordinates(self, ctx, action, *args):
        await ctx.message.delete()
        if ctx.channel.id == data.coordinate_channel:
            await task_list(ctx=ctx, action=action, args=args, use="bulletin")


class Task:
    def __init__(self, ctx, action, args):
        self.ctx = ctx
        self.action = action
        self.args = args

    # Check if the task already exists.
    def exists(args, channel_history):
        exists_already = False
        for message in channel_history:
            if message.embeds:
                title = message.embeds[0].title
                if title != discord.Embed.Empty:
                    if message.embeds[0].title in " ".join(args):
                        exists_already = True
                        return exists_already

        return exists_already

    # Delete a task from the list.
    def delete_task(args, channel_history):
        project = " ".join(args)
        for message in channel_history:
            if message.embeds:
                if message.embeds[0].title == project:
                    return message

    # Add a task to the list.
    def add_task(project, formatted, channel_history):
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

    # Remove a task from the list.
    def remove_task(project, value_list, channel_history):
        for message in channel_history:
            if message.embeds:
                if message.embeds[0].title == project:
                    bulletin_list = message.embeds[0].description.split("\n")
                    for i in value_list:
                        for j in bulletin_list:
                            if i in j:
                                bulletin_list.remove(j)
                    return bulletin_list, message

    # Rename a task.
    def rename_task(project, new_title, channel_history):
        if project[:-1] == " ":
            project = project[:-1]
        for message in channel_history:
            if message.embeds:
                if message.embeds[0].title == project:
                    edited_embed = discord.Embed(
                        color=0xe74c3c,
                        title=new_title,
                        description=message.embeds[0].description
                    )
                    return message, edited_embed

    # Generates the task list embed.
    async def task_list(ctx, action, use, args=""):
        # check for the correct syntax
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

        # Check for more syntax and perform the correct action.
        if action == "delete":
            await delete_task(args, channel_history).delete()
            return

        formatted, project, value_list = format_conversion(args, "bulletin")

        if not project:
            response = "I'm sorry but you didn't specify a project"
            await ctx.send(response, delete_after=5)
            return

        if not value_list:
            response = "I'm sorry but you didn't specify any other"
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
            message, embed = add_task(project, formatted, channel_history)
            await message.edit(embed=embed)
            return

        if action == "rename":
            title = " ".join(args).split("|")[1]
            message, embed = rename_task(project, title, channel_history)
            await message.edit(embed=embed)
            return

        if action == "remove":
            bulletin_list, message = remove_task(project, value_list, channel_history)
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

