from discord.ext import commands
import utilities.data as data


class JoinLeaveNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Check which user was the latest to join and store this in a global variable.
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.bot.enabled and not self.bot.debug:
            self.bot.latest_new_person = member

    # When the newest member leaves, there is a notification in th system channel.
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.bot.latest_new_person == member and self.bot.enabled and not self.bot.debug:
            response = 'Sadly, `{}` left us already.'.format(member.name)
            await self.bot.get_guild(data.hammer_guild).system_channel.send(response)