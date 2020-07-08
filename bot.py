# HammerBotPython
# bot.py

import discord
from discord.ext import commands
from dotenv import load_dotenv  # load module for usage of a .env file (pip install python-dotenv)
import os  # import module for directory management
import datetime
from discord.utils import get
from data import coordinate_channel, application_channel, vote_emotes, role_list, long_text
from coordinates import *
from utils import *
from bulletin import *

# discord token is stored in a .env file in the same directory as the bot
load_dotenv()  # load the .env file containing id's that have to be kept secret for security
TOKEN = os.getenv("DISCORD_TOKEN")  # get our discord bot token from .env
bot = commands.Bot(command_prefix="/")


# print a message if the bot is online
@bot.event
async def on_ready():
    print("bot connected")
    # change status to playing mc
    await bot.change_presence(activity=discord.Game("Technical Minecraft on HammerSMP"))


@bot.event
async def on_message(message):
    # check if the bot is online and not responding to itself
    if message.author == bot.user:
        return

    if message.channel.id == coordinate_channel:

        await message.delete()  # delete the message that was just sent
        """
        Check if the message is in the correct format.
        The format we want is the message to start with the dimension, i.e. _n or _ow.
        We also check if the message contains a ':' in the right spot, and checks that the coordinates are
        actual numbers.
        """
        if check_format(message):
            channel_history = await message.channel.history(limit=10).flatten()

            # if del is at the end of the message we want to delete that coordinate from the list
            if message.content[-3:] == "del":
                coordinate = message.content.strip(" del")

                # we also want to know if the coordinate is actually in the list, if tell that to the sender
                if not in_message(coordinate, channel_history):
                    await message.channel.send("This coordinate doesn't exist in the list.", delete_after=5)

                else:
                    # remove the coordinate from the list, get the message to edit and join the list back to a string
                    msg, edits = delete(coordinate, channel_history)
                    await msg.edit(content=edits)

            elif create_new_message(channel_history):
                if in_message(message.content, channel_history):
                    await message.channel.send("This coordinate is already in the list", delete_after=5)
                else:
                    await message.channel.send(message.content)

            else:
                if in_message(message.content, channel_history):
                    await message.channel.send("This coordinate is already in the list", delete_after=5)
                else:
                    # add the new message to the old message
                    coordinate_message = channel_history[0]
                    coordinate_list = coordinate_message.content
                    await coordinate_message.edit(content=coordinate_list + "\n" + message.content)
        else:
            await message.channel.send("Wrong format, please use the correct format", delete_after=5)


@bot.event
async def on_message(message):
    # check if the bot is online and not responding to itself
    if message.author == bot.user:
        return

    # if a new message is sent in the application forms channel, the bot will automatically add reactions
    if message.channel.id == application_channel:
        for e in vote_emotes:
            await message.add_reaction(bot.get_emoji(e))
    await bot.process_commands(message)  # makes sure other commands will also be processed


# command to test if the bot is running
@bot.command(name="test", help="test if the bot is working")
@commands.has_role("members")
async def test(ctx):
    response = "Don't worry, I'm working!"
    await ctx.send(response)


@bot.command(name="testing")
@commands.has_role("members")
async def testing(ctx):

    embed = discord.Embed(
        color=0xe74c3c,
        title="This is a test. How many characters can an Embed have?",
        description="some text"
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


# command to test if the bot is running
@bot.command(name="role", help="Give yourself the \"tour giver\" role")
@commands.has_role("members")
async def role(ctx, action, *args):
    if action == "list":
        await ctx.send(role_list)
        return

    # check if you have provided a role, if not tell the user to do so
    if args == ():
        response = "You have not specified a role"
        await ctx.send(response)
        return

    # combine the *args tuple into a string role
    role_arg = " ".join(args)

    # give the tour giver role if the user asks for this
    if role_arg in role_list:
        member = ctx.message.author  # the author of the message, part of the discord.Member class
        guild_role = get(member.guild.roles, name=role_arg)  # the role needed to add

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


# command to test if the bot is running
@bot.command(name="stop_lazy", help="command to tell someone to stop lazy")
@commands.has_role("members")
async def stop_lazy(ctx, mention="jerk"):
    response = "Stop Lazy {}".format(mention)
    await ctx.send(response)
    await ctx.send(file=discord.File('stop_lazy.png'))


@bot.command(name="CMP", help="command to get the CMP IP in your DM's")
@commands.has_any_role("CMP access", "members")
async def CMP(ctx, mention="jerk"):
    CMP_IP = os.getenv("CMP_IP")
    response = "Check your DM's"
    await ctx.author.send(CMP_IP)
    await ctx.send(response)


# command to test if the bot is running
@bot.command(name="vote", help="command to vote")
@commands.has_role("members")
async def vote(ctx, vote_type="", *args):
    await ctx.message.delete()

    if not args:
        response = "I'm sorry but you haven't specified anything to vote on."
        await ctx.send(response, delete_after=5)

    if not vote_type or vote_type not in ("yes_no", "multiple"):
        response = "I'm sorry but you haven't specified a correct vote type."
        await ctx.send(response, delete_after=5)

    if vote_type == "yes_no":
        string_votes = " ".join(args)
        embed = discord.Embed(
            color=0xe74c3c,
            title=string_votes,
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Poll created on {}".format(str(datetime.datetime.now())[:-7]))
        poll_message = await ctx.send(embed=embed)
        for e in vote_emotes:
            await poll_message.add_reaction(bot.get_emoji(e))

    elif vote_type == "multiple":
        poll, poll_list, introduction = format_conversion(args, "poll")
        embed = discord.Embed(
            color=0xe74c3c,
            title=introduction,
            description=poll[:-1]
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Poll created on {}".format(str(datetime.datetime.now())[:-7]))
        poll_message = await ctx.send(embed=embed)
        for n in range(len(poll_list)):
            await poll_message.add_reaction(discord_letters[n])


# /bulletin add project description | {first bulletin} & {second bulletin} & {third bulletin}
@bot.command(name="bulletin")
@commands.has_role("members")
async def bulletin(ctx, action, *args):
    await ctx.message.delete()
    if ctx.channel.id != coordinate_channel:
        response = "Sorry, wrong channel buddy"
        await ctx.send(response, delete_after=5)
        return

    channel_history = await ctx.channel.history(limit=50).flatten()
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
        await ctx.send(embed=embed)
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


# /bulletin add project description | {first bulletin} & {second bulletin} & {third bulletin}
@bot.command(name="todo")
@commands.has_role("members")
async def todo(ctx, action, *args):
    await ctx.message.delete()
    pins = await ctx.channel.pins()
    exists_already = exists(args, pins)

    if action == "delete":
        await delete_bulletin(args, pins).delete()
        return

    formatted, project, value_list = format_conversion(args, "bulletin")

    if not project:
        response = "I'm sorry but you didn't specify a title"
        await ctx.send(response, delete_after=5)
        return

    if not value_list:
        response = "I'm sorry but you didn't specify any todos"
        await ctx.send(response, delete_after=5)
        return

    if action == "create":
        if exists_already:
            response = "I'm sorry but this todo already exists"
            await ctx.send(response, delete_after=5)
            return

        embed = discord.Embed(
            color=0xe74c3c,
            title=project,
            description=formatted
        )
        todo = await ctx.send(embed=embed)
        await todo.pin()
        return

    if not exists_already:
        response = "I'm sorry but this todo doesn't exist"
        await ctx.send(response, delete_after=5)
        return

    if action == "add":
        message, edit_embed = add_bulletin(project, formatted, pins)
        print(edit_embed.title)
        await message.edit(embed=edit_embed)
        return

    if action == "remove":
        bulletin_list, message = remove_bulletin(project, value_list, pins)
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


bot.run(TOKEN)
