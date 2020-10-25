from discord.ext import commands, tasks

import cogs.help_command.help_data as hd
import utilities.data as data


def author_is_admin_or_dev(ctx):
    developers = [ctx.bot.get_user(_id) for _id in data.developer_ids]
    admin_role = ctx.bot.get_guild(data.hammer_guild).get_role(data.admin_role_id)
    return ctx.author in developers or admin_role in ctx.author.roles


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

    # This is a command purely for testing purposes during development.
    @commands.command(name='testing', help=hd.testing_help, usage=hd.testing_usage)
    @commands.check(author_is_admin_or_dev)
    async def testing(self, ctx, *args):
        await ctx.send("Nothing to test.")
