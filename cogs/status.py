import discord
from discord.ext import commands

import help_command.help_data as hd
import utilities.data as data


class Status(commands.Cog):
    """
    This cog is used to enable / disable the but and check the bots status. It uses 2 dummy commands.
    2 of the actions listen in on_message so they can listen to the /enable and /status commands even if
    the bot is disabled.

    This class also has the /ping command which will give the status and ping of the bot.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
    """

    def __init__(self, bot):
        self.bot = bot

    def get_self(self):
        return self

    @staticmethod
    def admin_or_dev_check(ctx):
        bot_dev = self.bot.get_user(234257395910443008)
        admin_role = self.bot.get_guild(data.hammer_guild).get_role(data.admin_role_id)
        return ctx.author == bot_dev or admin_role in ctx.author.roles

    @commands.command(name='disable', help=hd.disable_help, usage=hd.disable_usage)
    @commands.check(admin_or_dev_check)
    async def disable_bot(self, ctx):
        self.bot.enabled = False
        await ctx.send('Bot disabled!')
        print('Bot disabled')

    @commands.command(name='enable', help=hd.enable_help, usage=hd.enable_usage)
    @commands.check(self.admin_or_dev_check)
    async def enable_bot(self, ctx, *args):
        pass

    @commands.command(name='status', help=hd.status_help, usage=hd.status_usage)
    async def status(self, ctx, *args):
        pass

    # This command will provide the users with a way of testing if the bot is online.
    @commands.command(name='ping', help=hd.ping_help, usage=hd.ping_usage)
    async def ping(self, ctx):
        response = 'HammerBot Python is online and has a ping of {} ms.'.format(str(self.bot.latency)[:5])
        await ctx.send(response)
