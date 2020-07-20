# HammerBotPython
# bot.py

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os  # import module for directory management
from discord.ext import tasks

from Embeds import RichEmbed
from data import coordinate_channel, application_channel, vote_emotes, role_list, hammer_guild, role_ids, \
    vote_channel_id
from coordinates import *
from utils import *
from task import task_list
from bug import mc_bug
from voting import vote_handler

# discord token is stored in a .env file in the same directory as the bot
load_dotenv()  # load the .env file containing id's that have to be kept secret for security
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="/")

latest_new_person = ""


# Print a message if the bot is online and change it's status.
@bot.event
async def on_ready():
    print("bot connected")
    global latest_new_person
    await bot.change_presence(activity=discord.Game("Technical Minecraft on HammerSMP"))


@bot.event
async def on_message(message):
    # Make sure the bot doesn't respond to itself.
    if message.author == bot.user:
        return

    # Ff a new message is sent in the application forms channel, the bot will automatically add reactions.
    if message.channel.id == application_channel:
        for e in vote_emotes:
            await message.add_reaction(bot.get_emoji(e))

    await mc_bug(message)
    # We need this since since overriding the default provided on_message forbids any extra commands from running.
    await bot.process_commands(message)


# Check which user was the latest to join and store this in a global variable.0
@bot.event
async def on_member_join(member):
    global latest_new_person
    latest_new_person = member


# When the newest member leaves, there is a notification in th system channel.
@bot.event
async def on_member_remove(member):
    global latest_new_person
    if latest_new_person == member:
        response = "Sadly, **{}** left us already.".format(member.name)
        await bot.get_guild(hammer_guild).system_channel.send(response)


# Checking for new comments being added.
# on_raw_reaction_add is used since it is called regardless of the state of the internal message cache.
@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == vote_channel_id:
        pass


# This command will provide the users with a way of testing if the bot is online.
@bot.command(name="ping", help="Test if the bot is working.")
async def ping(ctx):
    response = "HammerBot Python is online, and has a ping of {} ms".format(str(bot.latency)[:5])
    await ctx.send(response)


# This is a command purely for testing purposes during development.
@bot.command(name="testing", help="A command purely used for development purposes.")
@commands.has_role("admin")
async def testing(ctx):
    await ctx.message.add_reaction("🔒")


# This command will be used so members can give themselves some roles wiht a command
@bot.command(name="role", help="Give yourself the \"tour giver\" or \"voten't giver\" role")
@commands.has_role("members")
async def role(ctx, action, *args):
    # This will send which roles a user can grant themselves.
    if action == "list":
        await ctx.send(role_list)
        return

    # check if you have provided a role, if not tell the user to do so
    if not args:
        response = "You have not specified a role"
        await ctx.send(response)
        return

    # combine the arguments tuple into a string role
    role_arg = " ".join(args)

    # give the role the user specified
    if role_arg in role_ids:
        member = ctx.message.author  # the author of the message, part of the discord.Member class
        guild_role = bot.get_guild(hammer_guild).get_role(role_ids[role_arg])  # the role needed to add

        if action == "add" and guild_role in member.roles:
            response = "I'm sorry but you already have this role"
            await ctx.send(response)
            return
        elif action == "remove" and guild_role not in member.roles:
            response = "I'm sorry but you don't have this role."
            await ctx.send(response)
            return

        # if the user doesn't have the right perms, throw an exception
        try:
            if action == "add":
                await member.add_roles(guild_role)
                response = "You have been successfully given the tour giver role! Congratulations."
                await ctx.send(response)

            elif action == "remove":
                await member.remove_roles(guild_role)
                response = "The role has successfully been removed, congratulations"
                await ctx.send(response)

        except discord.errors.Forbidden:
            response = "Missing permissions"
            await ctx.send(response)

    elif role_arg in get_server_roles(ctx):
        response = "I'm sorry but i'm afraid you can't add/remove that role to yourself using the bot."
        await ctx.send(response)

    # if the role is not a role one can add, throw an exception
    else:
        response = "I'm sorry but i'm afraid that role doesn't exist"
        await ctx.send(response)


# Tell someone to stop being lazy
@bot.command(name="stop_lazy", help="A command to tell someone to stop lazy.")
@commands.has_role("members")
async def stop_lazy(ctx, mention="jerk"):
    await ctx.message.delete()
    response = "Stop Lazy {}".format(mention)
    await ctx.send(response)
    await ctx.send(file=discord.File('stop_lazy.png'))


@bot.command(name="CMP", help="Command to get the CMP IP in your DM's")
@commands.has_any_role("CMP access", "members")
async def cmp(ctx):
    CMP_IP = os.getenv("CMP_IP")
    response = "Check your DM's"
    await ctx.author.send(CMP_IP)
    await ctx.send(response)


# Command that will handle voting, see voting.py.
@bot.command(name="vote", help="A voting command (stop complaining about unhelpful help command pls!")
@commands.has_role("members")
async def vote(ctx, vote_type="", *args):
    await ctx.message.delete()
    await vote_handler(ctx, vote_type, args, bot)


# Command to create, add, remove and delete bulletins in the bulletin board.
@bot.command(name="bulletin")
@commands.has_role("members")
async def bulletin(ctx, action, *args):
    await ctx.message.delete()
    """if ctx.channel.id != coordinate_channel:
        response = "Sorry, wrong channel buddy"
        await ctx.send(response, delete_after=5)
        return"""
    await task_list(ctx=ctx, action=action, args=args, use="bulletin")


# Command to add a to do list to a project channel and pin it.
@bot.command(name="todo")
@commands.has_role("members")
async def todo(ctx, action, *args):
    await ctx.message.delete()
    await task_list(ctx=ctx, action=action, args=args, use="todo")


# Command to handle the coordinate list. There is one embed per dimension
@bot.command(name="coordinates")
@commands.has_role("members")
async def coordinates(ctx, action, *args):
    await ctx.message.delete()
    if ctx.channel.id == coordinate_channel:
        await task_list(ctx=ctx, action=action, args=args, use="bulletin")


# A admin only command to mass delete messages in case of a bad discord discussion.
@bot.command(name="mass_delete")
@commands.has_role("admin")
async def mass_delete(ctx, number_of_messages):
    await ctx.message.delete()
    if number_of_messages > 200:
        response = "You want to delete too many messages at once, I'm sorry."
        await ctx.send(response)
    channel_history = await ctx.channel.history(limit=int(number_of_messages)).flatten()
    for message in channel_history:
        await message.delete()


# This will handle the errors thrown when using a certain command and tell the user if they are missing permissions.
@role.error
@testing.error
@ping.error
@stop_lazy.error
@cmp.error
@vote.error
@bulletin.error
@todo.error
@coordinates.error
@mass_delete.error
async def error(ctx, discord_error):
    if isinstance(discord_error, discord.ext.commands.MissingPermissions):
        await ctx.send("You don't have permission to do that!")

    elif isinstance(discord_error, discord.ext.commands.MissingRole):
        await ctx.send("You don't have the correct role to use that command!")


@tasks.loop(seconds=5)
async def forms():
    pass


forms.start()
bot.run(TOKEN)
