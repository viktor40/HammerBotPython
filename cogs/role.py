# HammerBotPython
# other module
# role.py

"""
role.py handles giving certain roles that members are allowed to give themselves.
These roles are used for notification and pinging purposes.
"""

import discord
from discord.ext import commands

from utilities.data import role_list, role_ids, hammer_guild
from utilities.utils import get_server_roles
import cogs.help_command.help_data as hd
import utilities.data as data
from utilities.utils import disable_for_debug


class Role(commands.Cog):
    """
    This cog is used to implement the role command.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
    """

    def __init__(self, bot):
        self.bot = bot
        print("> Role Cog Initialised")

    async def valid_argument(self, ctx, action, args):
        if action.lower() not in ['list', 'add', 'remove']:
            response = 'Invalid action.'
            await ctx.send(response)
            return False

        if not args:
            response = 'You have not specified a role'
            await ctx.send(response)
            return False

        return True

    async def user_has_role(self, ctx, action, role):
        has_role = self.bot.get_guild(hammer_guild).get_role(role_ids[role]) in ctx.message.author.roles
        if has_role and action == 'add':
            response = 'I am sorry but you already have this role.'
            await ctx.send(response)
            return False

        elif not has_role and action == 'remove':
            response = 'I am sorry but you don\'t have this role.'
            await ctx.send(response)
            return False

        else:
            return True

    async def role_checker(self, ctx, action, args):
        if not await self.valid_argument(ctx, action, args):
            return False

        role = ' '.join(args)
        if role not in get_server_roles(ctx):
            a = get_server_roles(ctx)
            response = 'I am sorry but i am afraid that role does not exist.'
            await ctx.send(response)
            return False

        elif role not in role_list:
            response = 'I am sorry but i am afraid you cannot add/remove that role to yourself using the bot.'
            await ctx.send(response)
            return False

        elif not await self.user_has_role(ctx, action, role):
            return False

        else:
            return True

    async def give_role(self, ctx, args):
        role = ' '.join(args)
        member = ctx.message.author  # the author of the message, part of the discord.Member class
        guild_role = self.bot.get_guild(hammer_guild).get_role(role_ids[role])  # the role needed to add
        await member.add_roles(guild_role)
        response = 'You have been successfully given the role `{}`! Congratulations!'.format(role)
        await ctx.send(response)

    async def remove_role(self, ctx, args):
        role = ' '.join(args)
        member = ctx.message.author  # the author of the message, part of the discord.Member class
        guild_role = self.bot.get_guild(hammer_guild).get_role(role_ids[role])  # the role needed to add
        await member.remove_roles(guild_role)
        response = 'The role `{}` has successfully been removed! Congratulations!'.format(role)
        await ctx.send(response)

    # This command will be used so members can give themselves some roles with a command
    @disable_for_debug
    @commands.command(name='role', help=hd.role_help, usage=hd.role_usage)
    @commands.has_role(data.member_role_id)
    async def role(self, ctx, action, *args):
        if not await self.role_checker(ctx, action, args):
            return

        if action == 'list':
            await ctx.send(role_list)
            return

        try:
            await self.give_role(ctx, args) if action == 'add' else await self.remove_role(ctx, args)

        except discord.errors.Forbidden:
            response = 'Missing permissions'
            await ctx.send(response)
