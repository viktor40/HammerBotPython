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
import time


async def create_task(task, ctx, action, use=''):
    await ctx.message.delete()
    await task.get_channel_history()
    task.search_history()
    pre_verification = task.verifier()
    if pre_verification:
        await ctx.send(pre_verification)
        return

    if action == 'delete':
        message = task.delete_task()
        await message.delete()

    elif action == 'remove':
        message = task.remove_task()
        await message.edit(embed=task.embed)

    elif action == 'create':
        task.create_task()
        message = await ctx.send(embed=task.embed)
        if use == 'todo':
            await message.pin()

    elif action == 'add':
        message = task.add_task()
        await message.edit(embed=task.embed)

    elif action == 'rename':
        message = task.rename_task()
        await message.edit(embed=task.embed)


class TaskCommand(commands.Cog):
    """
    This cog is used to implement the bulletin, to-do and coordinate command.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
    """

    def __init__(self, bot):
        self.bot = bot
        print('> {} Cog Initialised. Took {} s'.format('TaskCommand', time.perf_counter() - bot.start_time))
        bot.start_time = time.perf_counter()

    # Command to create, add, remove and delete bulletins in the bulletin board.
    @commands.command(name='bulletin', help=hd.bulletin_help, usage=hd.bulletin_usage)
    @commands.has_role(data.member_role_id)
    async def bulletin(self, ctx, action, *args):
        task = Bulletin(ctx, action, args, 'bulletin')
        await create_task(task, ctx, action)

    # Command to add a to do list to a project channel and pin it.
    @commands.command(name='todo', help=hd.todo_help, usage=hd.todo_usage)
    @commands.has_role(data.member_role_id)
    async def todo(self, ctx, action, *args):
        task = Todo(ctx, action, args, 'todo')
        await create_task(task, ctx, action, use='todo')

    # Command to handle the coordinate list. There is one embed per dimension
    @commands.command(name='coordinates', help=hd.coordinates_help, usage=hd.coordinates_usage)
    @commands.has_role(data.member_role_id)
    async def coordinates(self, ctx, action, *args):
        task = Coordinate(ctx, action, args, 'todo')
        await create_task(task, ctx, action)


class Task:
    def __init__(self, ctx, action, args, use):
        self.ctx = ctx
        self.action = action.lower()
        self.use = use.lower()
        self.args = args

        self.title, self.options = format_conversion(args)
        if self.options:
            self.bulletin_options = ['- {}'.format(option) if '- ' not in option else option for option in self.options]
        else:
            self.bulletin_option = None

        self.embed = discord.Embed(color=0xe74c3c)

        self.channel_history = None
        self.exist = False

    async def get_channel_history(self):
        self.channel_history = await self.ctx.channel.history(limit=50).flatten()

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

        if not self.options and self.action != 'delete':
            return 'No options specified.'

    def search_history(self, assign_to_self=False, find=False):
        for message in self.channel_history:
            if message.embeds and message.embeds[0].title == self.title:
                self.exist = True
                if assign_to_self:
                    self.embed = message
                    return message

                if find:
                    return message

    def create_task(self):
        self.embed.title = self.title
        self.embed.description = "\n".join(self.bulletin_options)

    def does_task_exist(self):
        self.search_history()

    def delete_task(self):
        return self.search_history(assign_to_self=True)

    def add_task(self):
        message = self.search_history(find=True)
        self.embed = discord.Embed(color=0xe74c3c,
                                   title=self.title,
                                   description=message.embeds[0].description + '\n' + '\n'.join(self.bulletin_options))
        return message

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


class Todo(Task):
    def __init__(self, ctx, action, args, use):
        super().__init__(ctx, action, args, use)

    async def get_channel_history(self):
        self.channel_history = await self.ctx.channel.pins()


class ChannelLockedTask(Task):
    def __init__(self, ctx, action, args, use, target_channel):
        super().__init__(ctx, action, args, use)
        self.target_channel = target_channel

    def verifier(self):
        basic_verification = super(ChannelLockedTask, self).verifier()
        if basic_verification:
            return basic_verification

        elif self.ctx.channel != self.target_channel:
            return 'This command can only be used in {}.'.format(self.target_channel.mention)


class Bulletin(ChannelLockedTask):
    def __init__(self, ctx, action, args, use):
        target_channel = ctx.get_channel(data.bulletin_board_channel)
        super().__init__(ctx, action, args, use, target_channel)


class Coordinate(ChannelLockedTask):
    def __init__(self, ctx, action, args, use):
        target_channel = ctx.get_channel(data.coordinate_channel)
        super().__init__(ctx, action, args, use, target_channel)
        self.coordinate_options = None

        self.x = None
        self.y = None
        self.z = None
        self.location = None

        self.max_length = 2000

    def verifier(self):
        basic_verification = super(Coordinate, self).verifier()
        if basic_verification:
            return basic_verification

        coordinate_verification = self.is_coordinate()
        if coordinate_verification:
            return coordinate_verification

    def is_coordinate(self):
        coordinates = self.options
        for coord in coordinates:
            title, positions = coord.split(': ')
            if len(positions) <= 1 or len(positions) > 3:
                return 'No proper coordinates provided.'

            else:
                for pos in positions:
                    if not pos.isnumeric():
                        return 'Coordinate isn\'t numeric.'

                self.decompose_coordinate(title, positions)

    def decompose_coordinate(self, title, positions):
        self.title = title
        for pos in positions:
            if len(pos) == 2:
                self.x = int(pos[0])
                self.y = 256
                self.z = int(pos[1])

            elif pos == 3:
                self.x = int(pos[0])
                self.y = int(pos[1])
                self.z = int(pos[2])

    def check_length(self, message):
        new_length = message.embeds[0].description + self.bulletin_options
        if new_length > self.max_length:
            return False
        else:
            return True

    def reorganise_embeds(self):
        pass

    def on_max_length_reached(self):
        pass
