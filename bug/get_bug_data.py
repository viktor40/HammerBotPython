# HammerBotPython
# bug module
# get_bug_data.py

"""
get_bug_data.py is as the name implies used to get and format different data from the bug tracker.
These methods are meant to be used in various places like getting bug data but also checking for fixed bugs.
"""

import datetime
import discord
import re


def set_description(issue, embed, max_length):
    description = issue.fields.description
    # limit the description length to 500 characters and add "..." to denote that there is more.
    if len(description) > 500:
        description = description[:500] + "..."

    # Add the variable we previously fetched to the embed
    embed.description = description
    return embed


def add_versions(issue, embed):
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
    return embed


def add_labels(issue, embed):
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
    return embed


def add_category(issue, embed):
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
    return embed


def add_assignee(issue, embed):
    # The same with assignee and priority. If there is none there will be an attribute error.
    try:
        embed.add_field(name='Assignee', value=issue.fields.assignee)
    except AttributeError:
        embed.add_field(name='Assignee', value='No Assignee')

    embed.add_field(name='Watchers', value=issue.fields.watches.raw['watchCount'])
    return embed


def add_priority(issue, embed):
    try:
        priority = issue.fields.customfield_12200
        if not priority:
            embed.add_field(name='Priority', value='None')

        else:
            embed.add_field(name='Priority', value=issue.fields.customfield_12200.value)

    except AttributeError:
        embed.add_field(name='Priority', value='No priority available')

    return embed


def add_image(issue, embed):
    # If there are attachments and they are an image, we add that image to tha embed.
    if issue.fields.attachment:
        for attach in issue.fields.attachment:
            regex = re.compile('(png|jpg|jpeg)')
            valid = re.findall(regex, attach.content)
            if valid:
                embed.set_image(url=attach.content)
                return embed
    return embed


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
