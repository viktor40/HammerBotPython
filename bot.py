# HammerBotPython
# main
# bot.py

"""
The source code can be found at:
https://github.com/viktor40/HammerBotPython

bot.py is the main file for the bot.
This file contains task loops for bug and version reporting as well as the main bot loop.

In this file we will check for different discord events like on_member_join, on_member_leave and on_message to handle
different tasks.

This file also contains all the commands that the bot listens to.
It also has dummy commands that are used by the help command so this bot lists the HammerBot Java commands too.

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
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

import bug.fixed as bug_fix
import bug.versions as mc_version

import utilities.data as data

from fun_zone.games.games import Games
from fun_zone.games.chess import ForbiddenChessMove

import cogs.help_command.help_data as hd
from cogs.dummy_commands import Dummy
from cogs.status import Status
from cogs.join_leave_notifier import JoinLeaveNotifier
from cogs.admin_commands import AdminCommands
from cogs.miscellaneous_commands import MiscellaneousCommands
from cogs.role import Role
from cogs.voting import Voting
from cogs.help_command.helping import Helping

# discord token is stored in a .env file in the same directory as the bot
load_dotenv()  # load the .env file containing id's that have to be kept secret for security
TOKEN = os.getenv('DISCORD_TOKEN')

DEBUG = True
if not DEBUG:
    prefix = "/"
else:
    prefix = "="

bot = commands.Bot(command_prefix=prefix, case_insensitive=True, help_command=None, intents=discord.Intents.all())

bot.latest_new_person = ""
bot.debug = DEBUG
bot.enabled = False
COGS = [Dummy, Status, JoinLeaveNotifier, Games, AdminCommands, MiscellaneousCommands, Role, Voting, Helping]


# Print a message if the bot is online and change it's status.
@bot.event
async def on_ready():
    print('bot connected')
    mc_version.get_versions(bot)
    bot.enabled = True
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

        # We need this since since overriding the default provided on_message forbids any extra commands from running.
        await bot.process_commands(message)


# Checking for new reactions being added.
# on_raw_reaction_add is used since it is called regardless of the state of the internal message cache.
@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == data.vote_channel_id:
        pass


# This will handle some errors and suppress raising them. It will also report to the user what the error was.
@bot.event
async def on_command_error(ctx, error):
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


# this loop is used to check for new updates on the bug tracker every 60 seconds
@tasks.loop(seconds=10, reconnect=True)
async def fixed_bug_loop():
    try:
        # on startup this is ran the first time but the bot isn't yet online so this would return []
        # to make sure it doesn't break we check for this
        channel = bot.get_channel(data.fixed_bug_channel_id)
        if channel:
            await bug_fix.fixes_handler(bot)

    # exceptions need to be handled, otherwise the loop might break
    except Exception as e:
        print(e)
        raise e


@tasks.loop(seconds=25, reconnect=True)
async def version_update_loop():
    try:
        # on startup this is ran the first time but the bot isn't yet online so this would return []
        # to make sure it doesn't break we check for this
        channel = bot.get_channel(data.fixed_bug_channel_id)
        if channel:
            await mc_version.version_update_handler(bot, channel)

    # exceptions need to be handled, otherwise the loop might break
    except Exception as e:
        print(e)


try:
    for cog in COGS:
        bot.add_cog(cog(bot))

    version_update_loop.start()  # start the loop to check for new versions
    fixed_bug_loop.start()  # start the loop to check for bugs
    bot.loop.run_until_complete(bot.start(TOKEN))

except KeyboardInterrupt:
    pass

finally:
    bot.loop.run_until_complete(bot.logout())
    print("done")
