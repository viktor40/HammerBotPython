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


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # This command will be used so members can give themselves some roles with a command
    @commands.command(name='role', help=hd.role_help, usage=hd.role_usage)
    @commands.has_role(data.member_role_id)
    async def role(self, ctx, action, *args):
        await role_giver(ctx, action, args, self.bot)


async def role_giver(ctx, action, args, bot):
    # This will send which roles a user can grant themselves.
    if action == 'list':
        await ctx.send(role_list)
        return

    # check if you have provided a role, if not tell the user to do so
    if not args:
        response = 'You have not specified a role'
        await ctx.send(response)
        return

    # combine the arguments tuple into a string role
    role_arg = ' '.join(args)

    # give the role the user specified
    if role_arg in role_ids:
        member = ctx.message.author  # the author of the message, part of the discord.Member class
        guild_role = bot.get_guild(hammer_guild).get_role(role_ids[role_arg])  # the role needed to add

        if action == 'add' and guild_role in member.roles:
            response = 'I am sorry but you already have this role.'
            await ctx.send(response)
            return

        elif action == 'remove' and guild_role not in member.roles:
            response = 'I am sorry but you does not have this role.'
            await ctx.send(response)
            return

        # if the user doesn't have the right perms, throw an exception
        try:
            if action == 'add':
                await member.add_roles(guild_role)
                response = 'You have been successfully given the tour giver role! Congratulations.'
                await ctx.send(response)

            elif action == 'remove':
                await member.remove_roles(guild_role)
                response = 'The role has successfully been removed, congratulations'
                await ctx.send(response)

        except discord.errors.Forbidden:
            response = 'Missing permissions'
            await ctx.send(response)

    elif role_arg in get_server_roles(ctx):
        response = 'I am sorry but i am afraid you cannot add/remove that role to yourself using the bot.'
        await ctx.send(response)

    # if the role is not a role one can add, throw an exception
    else:
        response = 'I am sorry but i am afraid that role does not exist.'
        await ctx.send(response)