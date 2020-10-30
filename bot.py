# HammerBotPython
# main
# bot.py

"""
The MIT License (MIT)

Copyright (c) 2020 Viktor40

The source code can be found at:
https://github.com/viktor40/HammerBotPython

bot.py is the main file for the bot.
This file contains task loops for bug and version reporting as well as the main bot loop.

In this file we will check for different discord events like on_member_join, on_member_leave and on_message to handle
different tasks.

This file also contains all the commands that the bot listens to.

Finally this file will also check for errors inside commands, but also in on_command_error. After an error gets
detected the bot will notify the user. The error message will be deleted after 15 seconds.

The required packages can be found in requirements.txt.
More info can be found in readme.md.

This also requires a .env file containing the following data:
DISCORD_TOKEN
CMP_IP
mojira_username
mojira_password

This file cannot be found on github for security reasons.
"""

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

import bug.versions as mc_version

import utilities.data as data

from fun_zone.games.games import Games
from fun_zone.games.chess import ForbiddenChessMove

from cogs.dummy_commands import DummyCommands
from cogs.status import Status
from cogs.join_leave_notifier import JoinLeaveNotifier
from cogs.admin_commands import AdminCommands
from cogs.miscellaneous_commands import MiscellaneousCommands
from cogs.role import Role
from cogs.voting import Voting
from cogs.help_command.helping import Helping
from cogs.task_command import TaskCommand
from cogs.bug_handler import BugHandler

# discord token is stored in a .env file in the same directory as the bot
TOKEN = os.getenv('DISCORD_TOKEN')

DEBUG = True
if not DEBUG:
    prefix = "/"
else:
    prefix = "="

COGS = [DummyCommands,  # Dummy commands
        Status,  # Bot status, disable, enable, ping ...
        JoinLeaveNotifier,  # Tracker for new people that join and immediately leave
        Games,  # Cog containing the different games implemented in the bot
        AdminCommands,  # Admin only or admin and dev only commands
        MiscellaneousCommands,  # Other commands not fit for a separate Cog
        Voting,  # Voting commands
        Helping,  # The help command
        Role,  # Commands to give people roles
        BugHandler,  # Showing of bugs from Mojang and tracking of fixed bugs and version releases
        TaskCommand  # Tasks: Coordinates, TO-DO and bulletins
        ]

bot = commands.Bot(command_prefix=prefix, case_insensitive=True, help_command=None, intents=discord.Intents.all())

bot.debug = DEBUG
bot.enabled = False


# Print a message if the bot is online and change it's status.
@bot.event
async def on_ready():
    print('----------------------------------------------------------')
    print('Bot connected with prefix: "{}"'.format(bot.command_prefix))
    if bot.debug:
        print('    > Debug mode is enabled.\n')

    print('The bot has connected to the following servers:')
    guilds = bot.guilds
    if not guilds:
        print("    > !! The bot isn't connected to any server. !!")

    for server in guilds:
        print("    > {}".format(server.name))
    print('----------------------------------------------------------')

    mc_version.get_versions(bot)
    bot.enabled = True
    bot.debug = DEBUG
    await bot.change_presence(activity=discord.Game('Technical Minecraft on HammerSMP'))


@bot.event
async def on_message(message):
    # Make sure the bot doesn't respond to itself.
    if message.author == bot.user:
        return

    if bot.enabled and not bot.debug:
        # Ff a new message is sent in the application forms channel, the bot will automatically add reactions.
        if message.channel.id == data.application_channel:
            for e in data.vote_emotes:
                await message.add_reaction(bot.get_emoji(e))

        await bot.process_commands(message)  # allow other commands to run


# This will handle some errors and suppress raising them. It will also report to the user what the error was.
@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("This command doesn't exist", delete_after=15)

    elif isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send("You don't have permission to do that!", delete_after=15)

    elif isinstance(error, discord.ext.commands.MissingRole):
        await ctx.send("You don't have the correct role to use that command!", delete_after=15)

    elif isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("I'm afraid you aren't allowed to use that command.", delete_after=15)

    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        if isinstance(error.original, ForbiddenChessMove):
            await ctx.send("This is not a valid move!", delete_after=15)

        else:
            print('unknown error: {} of type {}'.format(error, type(error)))
            await ctx.channel.send(error)
            if bot.debug:
                raise error

    else:
        print('unknown error: {} of type {}'.format(error, type(error)))
        await ctx.channel.send(error)
        if bot.debug:
            raise error

try:
    for cog in COGS:
        bot.add_cog(cog(bot))
    bot.loop.run_until_complete(bot.start(TOKEN))

except KeyboardInterrupt:
    pass

finally:
    bot.loop.run_until_complete(bot.logout())
    print("done")
