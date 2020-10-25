import discord
from discord.ext import commands

import help_command.help_data as hd
import utilities.data as data


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # A admin only command to mass delete messages in case of a bad discord discussion.
    @commands.command(name='mass_delete', help=hd.mass_delete_help, usage=hd.mass_delete_usage)
    @commands.has_role(data.admin_role_id)
    async def mass_delete(self, ctx, number_of_messages: int):
        await ctx.message.delete()
        if number_of_messages > 250:
            response = "You want to delete too many messages at once, I'm sorry."
            await ctx.send(response)
            return
        else:
            await ctx.channel.purge(limit=number_of_messages)
