# HammerBotPython
# bug module
# fixed.py

"""
fixed.py will check if new bugs are fixed. It will only does this for Minecraft java edition (code: mc).
It will check for both issues that have been resolved as fixed, and as won't fix in the last hour.
After that i'll check if the bug has already been sent to discord, if not we'll format it nicely in an embed
and send it over to discord.
"""

import datetime
import discord
from dotenv import load_dotenv
from jira import JIRA
import os
import re

from bug.fetcher import limited_bug
from bug.jira_filters import fixes_filter, no_fix_filter
from utilities.data import fixed_bug_channel_id

# Get the login details to login to the bug tracker.
load_dotenv()
mojira_username = os.getenv("mojira_username")
mojira_password = os.getenv("mojira_password")


# This will provide the embed showing the fixed bugs.
def fixed_bug_embed(jira_access, bug, status):
    # First we get the issue and get the basic embed template where we add some things to
    issue = jira_access.issue(bug)
    basic_embed = limited_bug(bug)

    # We change some attributes of the embed and add some extra ones. As well as an image.
    basic_embed.set_footer(text=bug_timedelta(issue))
    basic_embed.color = discord.Colour.green() if status == "Fixed" else discord.Colour.blue()
    marked = "**{}** was just resolved as **{}**!".format(bug.upper(), status)
    basic_embed.description = f'__{marked}__\n\n' \
                              f'{basic_embed.description}\n\n' \
                              f'{issue.fields.description[:300]} ...\n\n'

    if issue.fields.attachment:
        for attach in issue.fields.attachment:
            regex = re.compile("(png|jpg|jpeg)")
            valid = re.findall(regex, attach.content)
            if valid:
                basic_embed.set_image(url=attach.content)
                return basic_embed, marked
    return basic_embed, marked


# This function will just get the craation and resolution date and will then calculate the difference between them.
def bug_timedelta(issue):
    creation = issue.fields.created.split("T")[0]
    creation_date = datetime.date(year=int(creation.split("-")[0]),
                                  month=int(creation.split("-")[1]),
                                  day=int(creation.split("-")[2])
                                  )

    resolution = issue.fields.resolutiondate.split("T")[0]
    resolution_date = datetime.date(year=int(resolution.split("-")[0]),
                                    month=int(resolution.split("-")[1]),
                                    day=int(resolution.split("-")[2])
                                    )

    fix_time = resolution_date - creation_date
    footer = f'This issue was created on: {creation_date} and resolved on: {resolution_date}.\n' \
             f'The issue was open for {fix_time.days} days.'
    return footer


# Will filter for the latest bugs that have been resolved as fixed, or as won't fix and will add them to a list.
def new_fixes(jira_access):
    latest_fixed_bugs = jira_access.search_issues(fixes_filter)
    latest_wont_fix_bugs = jira_access.search_issues(no_fix_filter)
    fixes_list = [bug.key.lower() for bug in latest_fixed_bugs] if latest_fixed_bugs else None
    wont_fix_list = [bug.key.lower() for bug in latest_wont_fix_bugs] if latest_fixed_bugs else None
    return fixes_list, wont_fix_list, jira_access


# Here we check if the bug hasn't been sent already.
async def duplicate_checker(bot, bug):
    channel_history = await bot.get_channel(fixed_bug_channel_id).history(limit=30).flatten()
    for message in channel_history:
        if message.embeds:
            if bug.upper() in message.embeds[0].title:
                return True
    return False


# This will handle the main bug reporting
async def fixes_handler(bot):
    jira_access = JIRA(
        server='https://bugs.mojang.com',
        basic_auth=(mojira_username, mojira_password),
    )

    # First we get the list of newly resolved bugs that we're interested in
    fixes_list, wont_fix_list, jira_access = new_fixes(jira_access)
    bug_fix_channel = bot.get_channel(fixed_bug_channel_id)

    # Then we check for duplicates and finally we build the embed and send it to discord
    if fixes_list:
        for bug in fixes_list:
            if not await duplicate_checker(bot, bug):
                embed, status = fixed_bug_embed(jira_access, bug, status='Fixed')
                await bug_fix_channel.send(content=status, embed=embed)

    if wont_fix_list:
        for bug in wont_fix_list:
            if not await duplicate_checker(bot, bug):
                embed, status = fixed_bug_embed(jira_access, bug, status="Won't Fix")
                await bug_fix_channel.send(content=status, embed=embed)
