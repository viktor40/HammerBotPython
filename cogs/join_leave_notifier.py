from discord.ext import commands
import utilities.data as data


class JoinLeaveNotifier(commands.Cog):
    """
    This cog is used to implement the listeners for on_member_join and on_member_remove.
    We will store the latest person that joined. If they leave, a message will be sent in the system channel.

    Attributes:
        bot -- a discord.ext.commands.Bot object containing the bot's information
    """

    def __init__(self, bot):
        self.bot = bot
        self.latest_new_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.bot.enabled and not self.bot.debug:
            self.latest_new_member = member

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.latest_new_member == member and self.bot.enabled and not self.bot.debug:
            response = 'Sadly, `{}` left us already.'.format(member.name)
            await self.bot.get_guild(data.hammer_guild).system_channel.send(response)
