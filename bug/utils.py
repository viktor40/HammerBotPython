# HammerBotPython
# bug module
# utils.py

"""
This doesn't work yet and is still in development.
"""

import discord
from dotenv import load_dotenv
from jira import JIRA
import os

from bug.fetcher import limited_bug

# Get the login details to login to the bug tracker.
load_dotenv()
mojira_username = os.getenv('mojira_username')
mojira_password = os.getenv('mojira_password')


# This method will be used to vote for an open issue.
async def vote(bug):
    jira_access = JIRA(
        server='https://bugs.mojang.com',
        basic_auth=(mojira_username, mojira_password),
        async_=True
    )

    try:
        await jira_access.add_vote(bug)
    except Exception as e:
        print(e)
    issue = jira_access.issue(bug)
    votes = issue.fields.votes

    embed = limited_bug(bug)
    embed.color = discord.Colour.teal()
    embed.description = f'Issue {issue} has been voted on.\n' \
                        f'The issue now has a total of {votes} votes.'
    return embed
