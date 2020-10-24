import discord
from discord.ext import commands

import help_command.help_data as hd
import utilities.data as data


class Dummy(commands.Cog):
    """
    Registering dummy commands so it can be easily implemented to work with other functions like errors and help commands.
    These dummy commands are used in HammerBot Java.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='whitelist', help=hd.whitelist_help, usage=hd.whitelist_usage)
    @commands.has_role(data.admin_role_id)
    async def whitelist(self, ctx, *args):
        pass

    @commands.command(name='online', help=hd.online_help, usage=hd.online_usage)
    async def online(self, ctx, *args):
        pass

    @commands.command(name='scoreboard', help=hd.scoreboard_help, usage=hd.scoreboard_usage)
    async def scoreboard(self, ctx, *args):
        pass

    @commands.command(name='uploadFile', help=hd.upload_file_help, usage=hd.upload_file_usage)
    @commands.has_role(data.member_role_id)
    async def upload_file(self, ctx, *args):
        pass
