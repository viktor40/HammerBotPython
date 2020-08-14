# HammerBotPython
# other module
# voting.py

"""
voting.py will handle voting. It will put the vote in an embed. This embed will have the creator as author as well as
it's profile picture as the author icon. The bot will also automatically add voting options to the vote.
"""

import datetime
import discord

from other.task import format_conversion
from utilities.data import vote_role_id, vote_emotes, discord_letters


# This method can change the vote from to [closed] or [reopened]
def vote_status_change(channel_history, vote_type, args):
    # join the arguments into the title so we can look for it while iterating
    title = " ".join(args)
    for message in channel_history:
        if message.embeds:
            if title in message.embeds[0].title:
                embed_title = message.embeds[0].title
                if "[closed]" in embed_title:
                    embed_title = embed_title.replace("[closed]", "")
                if "[reopened]" in embed_title:
                    embed_title = embed_title.replace("[reopened]", "")
                edited_embed = discord.Embed(
                    color=0xe74c3c,
                    title="[{}] {}".format(vote_type, embed_title),
                    description=message.embeds[0].description
                )
                edited_embed.set_author(name=message.embeds[0].author.name, icon_url=message.embeds[0].author.icon_url)
                edited_embed.set_footer(text=str(message.embeds[0].footer.text))
                return message, edited_embed


# the vote handler will handle the creation of the different vote types and the formatting of the embeds
async def vote_handler(ctx, vote_type, args, bot):
    # If we don't have something to vote on throw an error.
    if not args:
        response = "I'm sorry but you haven't specified anything to vote on."
        await ctx.send(response, delete_after=5)

    # Throw an error in case the user used the wrong vote type
    if not vote_type or vote_type not in ("yes_no", "multiple", "reopen", "close"):
        response = "I'm sorry but you haven't specified a correct vote type."
        await ctx.send(response, delete_after=5)

    vote_role = ctx.guild.get_role(vote_role_id)

    # A vote which can only be answered by yes or no
    if vote_type == "yes_no":
        string_votes = " ".join(args)
        embed = discord.Embed(
            colour=0xe74c3c,
            title=string_votes
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Poll created on {}".format(str(datetime.datetime.now())[:-7]))
        poll_message = await ctx.send(content=vote_role.mention, embed=embed)

        # Add upvote, downvote and questionmark emote to vote for voting
        for e in vote_emotes:
            await poll_message.add_reaction(bot.get_emoji(e))

        # add lock emote to close the vote (not yet implemented)
        # await ctx.message.add_reaction("🔒")

    # A vote which has multiple options A, B, C ... which one can vote on
    elif vote_type == "multiple":
        poll, poll_list, introduction = format_conversion(args, "poll")
        embed = discord.Embed(
            color=0xe74c3c,
            title=introduction,
            description=poll[:-1] + " "
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Poll created on {}".format(str(datetime.datetime.now())[:-7]))
        poll_message = await ctx.send(content=vote_role.mention, embed=embed)

        # Add as many emotes as there are options
        for n in range(len(poll_list)):
            await poll_message.add_reaction(discord_letters[n])

        # await ctx.message.add_reaction("🔒")

    # close the vote
    elif vote_type == "close":
        channel_history = await ctx.channel.history(limit=6).flatten()
        message, edited_embed = vote_status_change(channel_history, "closed", args)
        await message.edit(embed=edited_embed)

    # reopen the vote
    elif vote_type == "reopen":
        channel_history = await ctx.channel.history(limit=6).flatten()
        message, edited_embed = vote_status_change(channel_history, "reopened", args)
        await message.edit(embed=edited_embed)
