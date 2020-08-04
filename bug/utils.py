import discord
from jira import JIRA
from dotenv import load_dotenv
import os

from bug.fetcher import limited_bug


# Get the login details to login to the bug tracker.
load_dotenv()
mojira_username = os.getenv("mojira_username")
mojira_password = os.getenv("mojira_password")


def vote(bruh_bug):
    bruh_jira_access = JIRA(
        server="https://bugs.mojang.com",
        basic_auth=(mojira_username, mojira_password),
    )

    bruh_jira_access.add_vote(bruh_bug)
    bruh_issue = bruh_jira_access.issue(bruh_bug)
    bruh_votes = bruh_issue.fields.votes

    bruh_embed = limited_bug(bruh_bug)
    bruh_embed.color = discord.Colour.teal()
    bruh_embed.description = f"Issue {bruh_issue} has been voted on.\n" \
                        f"The issue now has a total of {bruh_votes} votes."

    return bruh_embed
