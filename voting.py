from data import vote_role_id, vote_emotes, discord_letters
from task import format_conversion
import datetime
import discord


def vote_status_change(channel_history, vote_type, args):
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


async def vote_handler(ctx, vote_type, args, bot):
    if not args:
        response = "I'm sorry but you haven't specified anything to vote on."
        await ctx.send(response, delete_after=5)

    if not vote_type or vote_type not in ("yes_no", "multiple", "reopen", "close"):
        response = "I'm sorry but you haven't specified a correct vote type."
        await ctx.send(response, delete_after=5)

    vote_role = ctx.guild.get_role(vote_role_id)

    if vote_type == "yes_no":
        string_votes = " ".join(args)
        embed = discord.Embed(
            colour=0xe74c3c,
            title=string_votes,
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Poll created on {}".format(str(datetime.datetime.now())[:-7]))
        poll_message = await ctx.send(embed=embed)
        for e in vote_emotes:
            await poll_message.add_reaction(bot.get_emoji(e))
        # ping = await ctx.send(vote_role.mention)
        # await ping.delete()

    elif vote_type == "multiple":
        poll, poll_list, introduction = format_conversion(args, "poll")
        embed = discord.Embed(
            color=0xe74c3c,
            title=introduction,
            description=poll[:-1] + " "
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Poll created on {}".format(str(datetime.datetime.now())[:-7]))
        poll_message = await ctx.send(embed=embed)
        for n in range(len(poll_list)):
            await poll_message.add_reaction(discord_letters[n])
        # ping = await ctx.send(vote_role.mention)
        # await ping.delete()

    elif vote_type == "close":
        channel_history = await ctx.channel.history(limit=6).flatten()
        message, edited_embed = vote_status_change(channel_history, "closed", args)
        await message.edit(embed=edited_embed)

    elif vote_type == "reopen":
        channel_history = await ctx.channel.history(limit=6).flatten()
        message, edited_embed = vote_status_change(channel_history, "reopened", args)
        await message.edit(embed=edited_embed)
