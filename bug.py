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
print(regex)
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
                title=str.upper(issueid[0]),
                description=f"**{issue.fields.summary}**",
                url=f"https://bugs.mojang.com/browse/{issueid[0]}",
            )
            # embed.set_author(name=issue.fields., icon_url="")
            embed.add_field(name="Status", value=issue.fields.status)
            embed.add_field(name="Resolution", value=issue.fields.resolution)
            embed.add_field(name="Votes", value=issue.fields.votes)
            embed.set_footer(text=f"created: {issue.fields.created[:10]}")
            await message.channel.send(embed=embed)
        except:
            try:
                await message.channel.send(f"{issueid[0]} does not exist")
            except:
                await message.channel.send(f"fuck off {message.author.mention}")
        issue = jira.issue(issueid[0])

