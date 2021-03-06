from discord.ext import commands, tasks
import time
import bug.fixed as bug_fix
import bug.versions as mc_version
from bug.fetcher import mc_bug
import utilities.data as data


class BugHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not self.bot.debug:
            self.fixed_bug_loop.start()
            self.version_update_loop.start()
        print('> {} Cog Initialised. Took {} s'.format('BugHandler', time.perf_counter() - bot.start_time))
        bot.start_time = time.perf_counter()

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.enabled:
            print(message)
            await mc_bug(message)

    # this loop is used to check for new updates on the bug tracker every 60 seconds
    @tasks.loop(seconds=10, reconnect=True)
    async def fixed_bug_loop(self):
        try:
            # on startup this is ran the first time but the bot isn't yet online so this would return []
            # to make sure it doesn't break we check for this
            channel = self.bot.get_channel(data.fixed_bug_channel_id)
            if channel:
                await bug_fix.fixes_handler(self.bot)

        # exceptions need to be handled, otherwise the loop might break
        except Exception as e:
            print(e)
            raise e

    @tasks.loop(seconds=25, reconnect=True)
    async def version_update_loop(self):
        try:
            # on startup this is ran the first time but the bot isn't yet online so this would return []
            # to make sure it doesn't break we check for this
            channel = self.bot.get_channel(data.fixed_bug_channel_id)
            if channel:
                await mc_version.version_update_handler(self.bot, channel)

        # exceptions need to be handled, otherwise the loop might break
        except Exception as e:
            print(e)
