# HammerBotPython

import discord
from discord.ext import commands
from dotenv import load_dotenv  # load module for usage of a .env file (pip install python-dotenv)
import os  # import module for directory management
from discord.utils import get

# discord token is stored in a .env file in the same directory as the bot
load_dotenv()  # load the .env file containing id"s that have to be kept secret for security
TOKEN = os.getenv("DISCORD_TOKEN")  # get our discord bot token from .env
bot = commands.Bot(command_prefix="/")


# print a message if the bot is online
@bot.event
async def on_ready():
    print("bot connected")
    # change status to being gay
    await bot.change_presence(activity=discord.Game("Technical Minecraft"))


# command to test if the bot is running
@bot.command(name="test", help="test if the bot is working")
async def test(ctx):
    response = "Don\"t worry, I\"m working!"
    await ctx.send(response)


# command to test if the bot is running
@bot.command(name="role", help="Give yourself the 'tour giver' role")
# @commands.has_any_role("members") # only allows members to use the role
async def roles(ctx, *args):
    # check if you have provided a role, if not tell the user to do so
    if args == ():
        response = "You have been successfully given the tour giver role! Congratulations."
        await ctx.send(response)
        return

    # combine the *args tuple into a string role
    role = ""
    for i in args:
        role += i + " "
    role = role[:-1]

    # give the tour giver role if the user asks for this
    if role == "tour giver":
        member = ctx.message.author  # the author of the message, part of the discord.Member class
        role = get(member.guild.roles, name=role)  # the role needed to add

        # if the user doesn"t have the right perms, throw an exception
        try:
            await member.add_roles(role)
            response = "You have been successfully given the tour giver role! Congratulations."
            await ctx.send(response)

        except discord.errors.Forbidden:
            response = "Missing permissions"
            await ctx.send(response)

    # if the role is not a role one can add, throw an exception
    else:
        response = "I'm sorry but i'm afraid that role doesn't exist"
        await ctx.send(response)


bot.run(TOKEN)