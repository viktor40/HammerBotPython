# HammerBotPython
# bug module
# fetcher.py

"""
In fetcher.py bugs will be fetched from the bug tracker if they are mentioned in discord.
There are 2 different embeds, a small one containing only a small amount of info.
The 2nd embed is an extended one. The extended embed has a lot more information and thus is a bit larger.
"""

import discord
from dotenv import load_dotenv
import jira
from jira import JIRA
import os
import re

from bug.get_bug_data import *
from utilities.data import bug_colour_mappings

# The regex is used to check for bugs in teh correct format.
regex_normal = re.compile('((mc|mcapi|mcce|mcd|mcl|mcpe|mce|realms|web|bds)-[0-9]+)', re.IGNORECASE)

# Get the login details to login to the bug tracker.
load_dotenv()
mojira_username = os.getenv('mojira_username')
mojira_password = os.getenv('mojira_password')


# This will give a basic embed of a bug report to which someone can add or edit stuff for more specific embeds.
# This embed will also be used as a starting point for other bug related embeds.
def limited_bug(issueid):
    jira_access = JIRA(
        server='https://bugs.mojang.com',
        basic_auth=(mojira_username, mojira_password),
    )

    # Get the bug as an issue object.
    issue = jira_access.issue(issueid)

    # Now we will get different attributes from the bug and put them into a nice embed.
    status = issue.fields.status
    embed = discord.Embed(
        color=bug_colour_mappings[str(status)],
        title='**{}**: {}'.format(str.upper(issueid), issue.fields.summary),
        url=f'https://bugs.mojang.com/browse/{issueid}'
    )

    reporter = issue.fields.reporter.name.replace(" ", "+")
    embed.set_author(name=issue.fields.creator,
                     icon_url=getattr(issue.fields.reporter.avatarUrls, '48x48'),
                     url='https://bugs.mojang.com/secure/ViewProfile.jspa?name={}'.format(reporter)
                     )

    # Get the creation date and format status, resolution and votes.
    date_time = issue.fields.created.split("T")
    embed.set_footer(text='created on {} at {}'.format(date_time[0], date_time[1][:-9]))
    embed.description = '**Status:** {} | **Resolution:** {} | **Votes:** {}'.format(status,
                                                                                     issue.fields.resolution,
                                                                                     issue.fields.votes)
    return embed


# The extended bug embed will add extra info to the embed.
def extended_bug(issueid):
    jira_access = JIRA(
        server='https://bugs.mojang.com',
        basic_auth=(mojira_username, mojira_password),
    )

    # get different attributes from the but
    issue = jira_access.issue(issueid)
    status = issue.fields.status
    embed = limited_bug(issueid)

    embed = set_description(issue, embed, 500)
    embed.add_field(name='Status', value=status)
    embed.add_field(name='Resolution', value=issue.fields.resolution)
    embed.add_field(name='Votes', value=issue.fields.votes)

    embed = add_versions(issue, embed)
    embed = add_labels(issue, embed)
    embed = add_category(issue, embed)
    embed = add_category(issue, embed)
    embed = add_priority(issue, embed)
    embed = add_image(issue, embed)

    return embed


# This function is used to handle receiving and sending bug reports back to discord
async def mc_bug(message):
    # Convert the regex to usable issues.
    raw_issues = re.findall(regex_normal, message.content)

    # remove any duplicates in the message
    issues = []
    for bug in raw_issues:
        escape = f'%{bug[0].lower()}' not in message.content and f'%{bug[0].upper()}' not in message.content
        if bug not in issues and escape:
            issues.append(bug)

    # Extended will show a much more verbose embed with more info about the bug.
    extended = 'extended' in message.content

    if issues:
        # Iterate over the first 3 non duplicate bugs in the message
        for issueid in issues[:3]:
            try:
                if extended:
                    embed = extended_bug(issueid[0])
                    await message.channel.send(embed=embed)

                else:
                    embed = limited_bug(issueid[0])
                    await message.channel.send(embed=embed)

            except jira.exceptions.JIRAError:
                await message.channel.send(f'{issueid[0]} does not exist')
