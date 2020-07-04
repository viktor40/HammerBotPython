# HammerBotPython

import discord
from discord.ext import commands
from dotenv import load_dotenv  # load module for usage of a .env file (pip install python-dotenv)
import os  # import module for directory management

# discord token is stored in a .env file in the same directory as the bot
load_dotenv()  # load the .env file containing id's that have to be kept secret for security
TOKEN = os.getenv('DISCORD_TOKEN')  # get our discord bot token from .env
bot = commands.Bot(command_prefix='%')

# print a message if the bot is online
@bot.event
async def on_ready():
    print('bot connected')
    # change status to being gay
    await bot.change_presence(activity=discord.Game("Technical Minecraft"))


# command to test if the bot is running
@bot.command(name='test', help='test if the bot is working')
async def test(ctx):
    response = 'Don\'t worry, I\'m working!'
    await ctx.send(response)


# command to test if the bot is running
@bot.command(name='tour giver', help='test if the bot is working')
async def test(ctx):
    response = 'Don\'t worry, I\'m working!'
    await ctx.send(response)


bot.run(TOKEN)