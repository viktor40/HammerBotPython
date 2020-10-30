import discord
from discord.ext import commands
import os

import cogs.help_command.help_data as hd
import utilities.data as data
from utilities.utils import disable_for_debug


class MiscellaneousCommands(commands.Cog):
    """
    This cog is used to implement some miscellaneous commands.
    - stop_lazy: sends an image in discord to tell someone to "Stop Lazy". It takes a positional argument which can
                 contain an extra argument with custom text or an @ to mention someone.

    - CMP: The CMP command will DM the CMP IP to people with the CMP Access or member role.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
    """

    def __init__(self, bot):
        self.bot = bot
        print("> MiscellaneousCommands Cog Initialised")

    # Tell someone to stop being lazy
    @disable_for_debug
    @commands.command(name='stop_lazy', help=hd.stop_lazy_help, usage=hd.stop_lazy_usage)
    @commands.has_role(data.member_role_id)
    async def stop_lazy(self, ctx, mention='jerk'):
        await ctx.message.delete()
        response = 'Stop Lazy {}'.format(mention)
        await ctx.send(response)
        await ctx.send(file=discord.File('stop_lazy.png'))

    @disable_for_debug
    @commands.command(name='CMP', help=hd.CMP_help, usage=hd.CMP_usage)
    @commands.has_any_role(data.member_role_id, data.cmp_role_id)
    async def cmp(self, ctx):
        CMP_IP = os.getenv('CMP_IP')
        response = "Check your DM's"
        await ctx.author.send(CMP_IP)
        await ctx.send(response)

    @disable_for_debug
    @commands.command(name='count', help=hd.count_help, usage=hd.count_usage)
    async def count(self, ctx, count_type=''):
        if count_type.lower() == 'roles':
            roles = ctx.guild.roles
            description = {role: len(role.members) for role in roles}
            sorted_description = ["{}: {}".format(role.mention, count) for role, count in sorted(description.items(),
                                                                                                 key=lambda i: i[1])]
            count_embed = discord.Embed(title='members in {}'.format(ctx.guild.name),
                                        description='\n'.join(sorted_description[::-1]),
                                        color=discord.Color(0xFF7DD0))

        else:
            total_count = ctx.guild.member_count
            count_embed = discord.Embed(title='members in {}'.format(ctx.guild.name),
                                        description=total_count,
                                        color=discord.Color(0xFF7DD0)
                                        )

        await ctx.send(embed=count_embed)
