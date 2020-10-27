from discord.ext import commands, tasks
import bug.fixed as bug_fix
import bug.versions as mc_version
import cogs.help_command.help_data as hd
import utilities.data as data


class BugHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fixed_bug_loop.start()
        self.version_update_loop.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        # Make sure the bot doesn't respond to itself.
        if message.author == self.bot.user:
            return

        if self.bot.enabled and not self.bot.debug:
            # Ff a new message is sent in the application forms channel, the bot will automatically add reactions.
            if message.channel.id == data.application_channel:
                for e in data.vote_emotes:
                    await message.add_reaction(self.bot.get_emoji(e))

            await self.bot.process_commands(message)  # allow other commands to run

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
