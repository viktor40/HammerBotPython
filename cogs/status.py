import discord
from discord.ext import commands

import help_command.help_data as hd
import utilities.data as data


class Status(commands.Cog):
    """
    This cog is used to enable / disable the bot and check the bots status. It uses 2 dummy commands.
    2 of these commands are handled in on_message so they can listen to the /enable and /status commands even if
    the bot is disabled. The dummy commands are used so they are registered in bot.commands which is used for the
    help command

    This class also has the /ping command which will give the status and ping of the bot.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
    """

    def __init__(self, bot):
        self.bot = bot

    def author_is_admin_or_dev(self):
        def predicate(ctx):
            developers = [self.bot.get_user(_id) for _id in data.developer_ids]
            admin_role = self.bot.get_guild(data.hammer_guild).get_role(data.admin_role_id)
            return ctx.author in developers or admin_role in ctx.author.roles
        return predicate

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.lower() == "{}status".format(self.bot.command_prefix):
            await message.channel.send('Bot enabled = {}!'.format(self.bot.enabled))

        if not self.bot.enabled:
            if message.content.lower() == "{}enable".format(self.bot.command_prefix):
                self.bot.enabled = True
                await message.channel.send('Bot enabled!')
                print('Bot enabled!')

        return

    @commands.command(name='disable', help=hd.disable_help, usage=hd.disable_usage)
    @commands.check(author_is_admin_or_dev)
    async def disable_bot(self, ctx):
        self.bot.enabled = False
        await ctx.send('Bot disabled!')
        print('Bot disabled')

    @commands.command(name='enable', help=hd.enable_help, usage=hd.enable_usage)
    @commands.check(author_is_admin_or_dev)
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
