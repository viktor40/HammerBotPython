# HammerBotPython
# bug_fetcher.py

import discord
import re
from jira import JIRA
import jira
from dotenv import load_dotenv
import os
from utilities.data import bug_colour_mappings

# The regex is used to check for bugs in teh correct format.
regex_normal = re.compile("((mc|mcapi|mcce|mcd|mcl|mcpe|mce|realms|web|bds)-[0-9]+)", re.IGNORECASE)

# Get the login details to login to the bug tracker.
load_dotenv()
mojira_username = os.getenv("mojira_username")
mojira_password = os.getenv("mojira_password")


async def mc_bug(message):
    # Convert the regex to usable issues.
    raw_issues = re.findall(regex_normal, message.content)

    # remove any duplicates in the message
    issues = []
    for bug in raw_issues:
        if bug not in issues:
            issues.append(bug)

    # Extended will show a much more verbose embed with more info about the bug.
    extended = "extended" in message.content

    if issues:
        # Login to the bug tracker.
        jira_access = JIRA(
            server="https://bugs.mojang.com",
            basic_auth=(mojira_username, mojira_password),
        )

        # Iterate over the first 3 non duplicate bugs in the message
        for issueid in issues[:3]:
            try:
                issue = jira_access.issue(issueid[0])
                status = issue.fields.status
                embed = discord.Embed(
                    color=bug_colour_mappings[str(status)],
                    title="**{}**: {}".format(str.upper(issueid[0]), issue.fields.summary),
                    url=f"https://bugs.mojang.com/browse/{issueid[0]}")
                embed.set_author(name=issue.fields.creator,
                                 icon_url=getattr(issue.fields.reporter.avatarUrls, "48x48"),
                                 url="https://bugs.mojang.com/secure/ViewProfile.jspa?name={}".format(issue.fields.reporter.name))
                date_time = issue.fields.created.split("T")
                embed.set_footer(text="created on {} at {}".format(date_time[0], date_time[1][:-9]))

                if extended:

                    description = issue.fields.description

                    if len(description) > 500:
                        description = description[:500] + "..."
                    embed.description = description
                    embed.add_field(name="Status", value=status)
                    embed.add_field(name="Resolution", value=issue.fields.resolution)
                    embed.add_field(name="Votes", value=issue.fields.votes)

                    versions = issue.fields.versions
                    if len(versions) > 4:
                        version_field = "{},\n{}\n...\n{},\n{}".format(versions[0].name, versions[1].name,
                                                                       versions[-2].name, versions[-1].name)
                    else:
                        version_field = ""
                        for version in versions:
                            version_field += version.name + ",\n"
                        version_field = version_field[:-2]
                    embed.add_field(name="Versions", value=version_field)
                    labels = issue.fields.labels
                    label_field = ""
                    if not labels:
                        label_field = "None"
                    else:
                        for label in labels:
                            label_field += label + "\n"
                        label_field = label_field[:-1]
                    embed.add_field(name="Labels", value=label_field)
                    try:
                        categories = issue.fields.customfield_11901
                        category_field = ""
                        if not categories:
                            category_field = "None"
                        else:
                            for category in categories:
                                category_field += str(category) + "\n"
                    except AttributeError:
                        category_field = "No categories available"

                    embed.add_field(name="Category", value=category_field)
                    embed.add_field(name="Assignee", value=issue.fields.assignee)
                    embed.add_field(name="Watchers", value=issue.fields.watches.raw["watchCount"])
                    try:
                        priority = issue.fields.customfield_12200
                        if not priority:
                            embed.add_field(name="Priority", value="None")
                        else:
                            embed.add_field(name="Priority", value=issue.fields.customfield_12200.value)
                    except AttributeError:
                        embed.add_field(name="Priority", value="No priority available")

                    if issue.fields.attachment:
                        for attach in issue.fields.attachment:
                            regex = re.compile("(png|jpg|jpeg)")
                            valid = re.findall(regex, attach.content)
                            if valid:
                                embed.set_image(url=attach.content)
                                await message.channel.send(embed=embed)
                                return
                    await message.channel.send(embed=embed)

                else:
                    embed.description = "**Status:** {} | **Resolution:** {} | **Votes:** {}".format(status, issue.fields.resolution, issue.fields.votes)
                    await message.channel.send(embed=embed)

            except jira.exceptions.JIRAError:
                try:
                    await message.channel.send(f"{issueid[0]} does not exist")
                except:
                    await message.channel.send(f"fuck off {message.author.mention}")