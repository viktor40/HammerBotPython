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


async def create_task(ctx, action, args, use):
    task = Task(ctx, action, args, use)
    task.search_history()
    pre_verification = task.verifier()
    if pre_verification:
        await ctx.send(pre_verification)
        return

    if action == 'delete':
        task.delete_task()
        await ctx.send(embed=task.embed)

    elif action == 'remove':
        task.remove_task()
        await ctx.send(embed=task.embed)

    elif action == 'create':
        task.create_task()
        await ctx.send(embed=task.embed)

    elif action == 'add':
        task.add_task()
        await ctx.send(embed=task.embed)

    elif action == 'rename':
        task.rename_task()
        await ctx.send(embed=task.embed)


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
        await create_task(ctx=ctx, action=action, args=args, use="bulletin")

    # Command to add a to do list to a project channel and pin it.
    @commands.command(name='todo', help=hd.todo_help, usage=hd.todo_usage)
    @commands.has_role(data.member_role_id)
    async def todo(self, ctx, action, *args):
        await create_task(ctx=ctx, action=action, args=args, use="todo")

    # Command to handle the coordinate list. There is one embed per dimension
    @commands.command(name='coordinates', help=hd.coordinates_help, usage=hd.coordinates_usage)
    @commands.has_role(data.member_role_id)
    async def coordinates(self, ctx, action, *args):
        await ctx.message.delete()
        if ctx.channel.id == data.coordinate_channel:
            await self.task_list(ctx=ctx, action=action, args=args, use="bulletin")


class Task:
    def __init__(self, ctx, action, args, use):
        self.ctx = ctx
        self.action = action.lower
        self.use = use.lower()
        self.args = args

        self.title, self.options = format_conversion(args)
        self.bulletin_options = ['- {}'.format(option) if '- ' not in option else option for option in self.options]
        self.embed = discord.Embed(color=0xe74c3c)

        self.channel_history = None
        self.get_channel_history()
        self.exist = False

    def verifier(self):
        if self.use not in ['bulletin', 'todo', 'coordinate']:
            return 'Wrong use specified.'

        if self.action not in ['delete', 'create', 'add', 'rename', 'remove']:
            return 'Wrong action specified.'

        elif self.action in ['delete', 'add', 'rename', 'remove'] and not self.exist:
            return 'This {} does not exist.'.format(self.use)

        elif self.action == 'create' and self.exist:
            return 'This {} can\'t be created. It already exists.'.format(self.use)

        if not self.args:
            return 'No arguments have been specified.'

        if not self.title:
            return 'No title specified.'

        if not self.options:
            return 'No options specified.'

    def get_channel_history(self):
        if self.use == "bulletin" and self.ctx.channel == self.ctx.bot.get_channel():
            self.channel_history = await self.ctx.channel.history(limit=50).flatten()

        elif self.use == "todo":
            self.channel_history = await self.ctx.channel.pins()

    def search_history(self, assign_to_self=False, find=False):
        for message in self.channel_history:
            if message.embeds:
                if message.embeds[0].title == self.title:
                    self.exist = True
                    if assign_to_self:
                        self.embed = message

                    if find:
                        return message

    def create_task(self):
        self.embed.title = self.title
        self.embed.description = "\n".join(self.bulletin_options)

    def does_task_exist(self):
        self.search_history()

    def delete_task(self):
        self.search_history(assign_to_self=True)

    def add_task(self):
        message = self.search_history(find=True)
        self.embed = discord.Embed(color=0xe74c3c,
                                   title=self.title,
                                   description=message.embeds[0].description + self.bulletin_options)

    def remove_task(self):
        message = self.search_history(find=True)
        bulletin_list = message.embeds[0].description.split("\n")
        for i in self.bulletin_options:
            if i in bulletin_list:
                bulletin_list.remove(i)

        self.embed = discord.Embed(color=0xe74c3c,
                                   title=self.title,
                                   description='\n'.join(bulletin_list))
        return message

    def rename_task(self):
        message = self.search_history(find=True)
        self.embed = discord.Embed(color=0xe74c3c,
                                   title=self.options[0],
                                   description=message.embeds[0].description)
        return message


class Coordinate(Task):
    def __init__(self, ctx, action, args, use):
        super().__init__(ctx, action, args, use)
        self.target_channel = ctx.get_channel(data.coordinate_channel)
        self.max_length = 2000

    def verifier(self):
        basic_verification = super(Coordinate, self).verifier()
        if basic_verification:
            return basic_verification

        elif self.ctx.channel != self.target_channel:
            return 'This command can only be used in {}.'.format(self.target_channel.mention)

    def check_length(self):
        pass

    def exceeds_max_length(self):
        pass
