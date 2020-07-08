# HammerBotPython
# bug.py

import discord
import re
from jira import JIRA
from dotenv import load_dotenv  # load module for usage of a .env file (pip install python-dotenv)
import os  # import module for directory management

regex = re.compile(
    "((mc|mcapi|mcce|mcds|mcl|mcpe|realms|sc|web)-[0-9]+)", re.IGNORECASE
)

load_dotenv()  # load the .env file containing id's that have to be kept secret for security
mojira_username = os.getenv("mojira_username")
mojira_password = os.getenv("mojira_password")


async def mc_bug(message, issues):
    jira = JIRA(
        server="https://bugs.mojang.com",
        basic_auth=(mojira_username, mojira_password),
    )

    for issueid in issues:
        try:
            issue = jira.issue(issueid[0])
            embed = discord.Embed(
                color=discord.Colour.orange(),
                title="**{}**: {}".format(str.upper(issueid[0]), issue.fields.summary),
                description="**Status:** {} | **Resolution:** {} | **Votes:** {}".format(issue.fields.status,
                                                                                         issue.fields.resolution,
                                                                                         issue.fields.votes),
                url=f"https://bugs.mojang.com/browse/{issueid[0]}",
            )
            date_time = issue.fields.created.split("T")
            embed.set_footer(text="created on {} at {}".format(date_time[0], date_time[1][:-9]))
            embed.set_author(name=issue.fields.creator, icon_url=getattr(issue.fields.reporter.avatarUrls, "48x48"))
            await message.channel.send(embed=embed)
        except:
            try:
                await message.channel.send(f"{issueid[0]} does not exist")
            except:
                await message.channel.send(f"fuck off {message.author.mention}")
