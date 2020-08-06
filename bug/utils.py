# HammerBotPython
# bug module
# utils.py

"""
This doesn't work yet and is still in development.
"""

import discord
from jira import JIRA
from dotenv import load_dotenv
import os

from bug.fetcher import limited_bug

# Get the login details to login to the bug tracker.
load_dotenv()
mojira_username = os.getenv('mojira_username')
mojira_password = os.getenv('mojira_password')


# This method will be used to vote for an open issue.
def vote(bug):
    jira_access = JIRA(
        server='https://bugs.mojang.com',
        basic_auth=(mojira_username, mojira_password),
    )

    jira_access.add_vote(bug)
    issue = jira_access.issue(bug)
    votes = issue.fields.votes

    embed = limited_bug(bug)
    embed.color = discord.Colour.teal()
    embed.description = f'Issue {issue} has been voted on.\n' \
                        f'The issue now has a total of {votes} votes.'
    return embed