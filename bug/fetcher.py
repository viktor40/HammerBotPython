# HammerBotPython
# bug module
# fetcher.py

"""
In fetcher.py bugs will be fetched from the bug tracker if they are mentioned in discord.
There are 2 different embeds, a small one containing only a small amount of info.
The 2nd embed is an extended one. The extended embed has a lot more information and thus is a bit larger.
"""

import discord
import re
from jira import JIRA
import jira
from dotenv import load_dotenv
import os
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
    description = issue.fields.description

    # limit the description length to 500 characters and add "..." to denote that there is more.
    if len(description) > 500:
        description = description[:500] + "..."

    # Add the variable we previously fetched to the embed
    embed.description = description
    embed.add_field(name='Status', value=status)
    embed.add_field(name='Resolution', value=issue.fields.resolution)
    embed.add_field(name='Votes', value=issue.fields.votes)

    # Get the affected versions, format them only showing the first and last 2 and ignoring all other versions.
    # If there are less than 4 versions, we show all of them. Then we add a field and value containing the data.
    versions = issue.fields.versions
    if len(versions) > 4:
        version_field = '{},\n{}\n...\n{},\n{}'.format(versions[0].name, versions[1].name,
                                                       versions[-2].name, versions[-1].name)
    else:
        version_field = ""
        for version in versions:
            version_field += version.name + ",\n"
        version_field = version_field[:-2]
    embed.add_field(name='Versions', value=version_field)

    # Get the labels, if there are none, display that. If there are format them with newlines in between.
    labels = issue.fields.labels
    label_field = ''
    if not labels:
        label_field = 'None'
    else:
        for label in labels:
            label_field += label + '\n'
        label_field = label_field[:-1]
    embed.add_field(name='Labels', value=label_field)

    # This is in a try and except since not all bugs have this attribute. Tis will make sure that there isn't an error
    # stopping the function prematurely. We also format the different categories with newlines.
    try:
        categories = issue.fields.customfield_11901
        category_field = ''
        if not categories:
            category_field = 'None'
        else:
            for category in categories:
                category_field += str(category) + '\n'
    except AttributeError:
        category_field = 'No categories available'
    embed.add_field(name='Category', value=category_field)

    # The same with assignee and priority. If there is none there will be an attribute error.
    try:
        embed.add_field(name='Assignee', value=issue.fields.assignee)
    except AttributeError:
        embed.add_field(name='Assignee', value='No Assignee')

    embed.add_field(name='Watchers', value=issue.fields.watches.raw['watchCount'])

    try:
        priority = issue.fields.customfield_12200
        if not priority:
            embed.add_field(name='Priority', value='None')
        else:
            embed.add_field(name='Priority', value=issue.fields.customfield_12200.value)
    except AttributeError:
        embed.add_field(name='Priority', value='No priority available')

    # If there are attachments and they are an image, we add that image to tha embed.
    if issue.fields.attachment:
        for attach in issue.fields.attachment:
            regex = re.compile('(png|jpg|jpeg)')
            valid = re.findall(regex, attach.content)
            if valid:
                embed.set_image(url=attach.content)
                return embed
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
