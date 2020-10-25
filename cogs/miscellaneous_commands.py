import discord
from discord.ext import commands
import os

import cogs.help_command.help_data as hd
import utilities.data as data


class MiscellaneousCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Tell someone to stop being lazy
    @commands.command(name='stop_lazy', help=hd.stop_lazy_help, usage=hd.stop_lazy_usage)
    @commands.has_role(data.member_role_id)
    async def stop_lazy(self, ctx, mention='jerk'):
        await ctx.message.delete()
        response = 'Stop Lazy {}'.format(mention)
        await ctx.send(response)
        await ctx.send(file=discord.File('stop_lazy.png'))

    @commands.command(name='CMP', help=hd.CMP_help, usage=hd.CMP_usage)
    @commands.has_any_role(data.member_role_id, data.cmp_role_id)
    async def cmp(self, ctx):
        CMP_IP = os.getenv('CMP_IP')
        response = "Check your DM's"
        await ctx.author.send(CMP_IP)
        await ctx.send(response)
