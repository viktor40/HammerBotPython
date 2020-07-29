# HammerBotPython
# bug module
# fixed.py

import discord
from jira import JIRA
from dotenv import load_dotenv
import os
from utilities.data import fixed_bug_channel_id
from bug.fetcher import limited_bug
import re

# Get the login details to login to the bug tracker.
load_dotenv()
mojira_username = os.getenv("mojira_username")
mojira_password = os.getenv("mojira_password")


def fixed_bug_embed(jira_access, bug, status):
    issue = jira_access.issue(bug)
    basic_embed = limited_bug(bug)
    basic_embed.color = discord.Colour.green() if status == "Fixed" else discord.Colour.blue()
    marked = "This ticket was just resolved as {}!".format(status)
    basic_embed.description = f'**{marked}**\n\n{basic_embed.description}\n\n{issue.fields.description[:300]} ...'

    if issue.fields.attachment:
        for attach in issue.fields.attachment:
            regex = re.compile("(png|jpg|jpeg)")
            valid = re.findall(regex, attach.content)
            if valid:
                basic_embed.set_image(url=attach.content)
                return basic_embed
    return basic_embed


def new_fixes(jira_access):
    fixes_filter = "project = MC AND status = Resolved AND resolution = Fixed AND resolved >= -3m ORDER BY updated DESC"
    no_fix_filter = "project = MC AND status = Resolved AND resolution = \"Won't Fix\" AND resolved >= -3m ORDER BY updated DESC"
    latest_fixed_bugs = jira_access.search_issues(fixes_filter)
    latest_wont_fix_bugs = jira_access.search_issues(no_fix_filter)
    fixes_list = [bug.key.lower() for bug in latest_fixed_bugs] if latest_fixed_bugs else None
    wont_fix_list = [bug.key.lower() for bug in latest_wont_fix_bugs] if latest_fixed_bugs else None
    return fixes_list, wont_fix_list, jira_access


async def duplicate_checker(bot, bug):
    channel_history = await bot.get_channel(fixed_bug_channel_id).history(limit=30).flatten()
    for message in channel_history:
        if message.embeds:
            if bug.upper() in message.embeds[0].title:
                return True
    return False


async def fixes_handler(bot):
    jira_access = JIRA(
        server="https://bugs.mojang.com",
        basic_auth=(mojira_username, mojira_password),
    )

    fixes_list, wont_fix_list, jira_access = new_fixes(jira_access)
    bug_fix_channel = bot.get_channel(fixed_bug_channel_id)
    if fixes_list:
        for bug in fixes_list:
            if not await duplicate_checker(bot, bug):
                status = "This ticket was just resolved as \"Fixed\"!"
                await bug_fix_channel.send(content=status, embed=fixed_bug_embed(jira_access, bug, status="Fixed"))

    if wont_fix_list:
        for bug in wont_fix_list:
            if not await duplicate_checker(bot, bug):
                status = "This ticket was just resolved as \"Won't Fix\"!"
                await bug_fix_channel.send(content=status, embed=fixed_bug_embed(jira_access, bug, status="Won't Fix"))
