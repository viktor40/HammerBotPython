# HammerBotPython
# bug module
# versions.py

"""
versions.py checks for new and archived versions on the mojang bug tracker.
It will only does this for Minecraft java edition (code: mc).
If a new version has been found or an old one has been archived it will be formatted into an embed.
It will also list the affected bugs and fixed bugs in that version.
"""

from jira import JIRA
import os
from dotenv import load_dotenv
import discord

from bug.jira_filters import affected_filter, number_fixed_filter

# Get the sensitive data to log in to the bug tracker from the .env file.
load_dotenv()
mojira_username = os.getenv("mojira_username")
mojira_password = os.getenv("mojira_password")


# This method gets called once on the initialisation of the bot. It will create bot variables for the latest versions
# and other data relating to versions. These will be changed later in the same instance of the bot if a new
# version has been detected, or an old one has been archived.
def get_versions(bot):
    jira_access = JIRA(
        server="https://bugs.mojang.com",
        basic_auth=(mojira_username, mojira_password),
    )
    versions = jira_access.project("MC").versions
    bot.mc_versions = {str(version) for version in versions}

    bot.latest_version = str(versions[-1])
    bot.previous_version = str(versions[-2])
    bot.latest_version_archive_status = versions[-1].archived
    bot.previous_version_archive_status = versions[-2].archived
    bot.latest_version_release_status = versions[-1].released


# This method will get the number of bugs that a certain filter returns.
def get_from_filter(jira_filter, jira_access):
    filter_list = jira_access.search_issues(jira_filter, maxResults=False)
    filter_len = len(filter_list)
    return filter_len


# This method checks for the different affected bugs.
def affected_bugs(version, jira_access):
    jira_filter = affected_filter.format(version)
    number_affected = get_from_filter(jira_filter, jira_access)
    return number_affected


# This method checks for the different fixed bugs.
def fixed_bugs(version, jira_access):
    jira_filter = number_fixed_filter.format(version)
    number_fixes = get_from_filter(jira_filter, jira_access)
    return number_fixes


# This method checks for new versions. If a new one has been detected it'll change the bot variables.
def new_version(bot, versions):
    latest_version = versions[-1]
    if bot.latest_version != str(versions[-1]):
        bot.previous_version = bot.latest_version
        bot.latest_version = str(versions[-1])
        bot.previous_version_archive_status = bot.latest_version_archive_status
        bot.latest_version_archive_status = latest_version.archived
        bot.latest_version_release_status = latest_version.released
        return latest_version

    else:
        return None


# This method checks for archived versions. If a new one has been detected it'll change the bot variables.
def archived_version(bot, versions):
    previous_version = versions[-2]
    if not bot.previous_version_archive_status and previous_version.archived:
        bot.previous_version_archive_status = previous_version.archived
        return previous_version

    else:
        return None


# This method checks for released versions. If a new one has been detected it'll change the bot variables.
def released_version(bot, versions):
    latest_version = versions[-1]
    if not bot.latest_version_release_status and latest_version.released:
        bot.latest_version_release_status = latest_version.released
        return latest_version

    else:
        return None


# The version reporter will create an embed containing the info we want to send in the channel.
def version_update_reporter(bot):
    jira_access = JIRA(
        server="https://bugs.mojang.com",
        basic_auth=(mojira_username, mojira_password),
    )

    # All the different minecraft versions on the bug tracker
    versions = jira_access.project("MC").versions

    embed = discord.Embed(color=discord.Colour.magenta())

    # We check for the different kinds of version changes.
    # We can just return after that since updates between the different version updates will never be faster
    # than the period of the loop.

    # Check for new versions, if there are we send the embed containing that info.
    new = new_version(bot, versions)
    if new:
        embed.title = str(new)
        embed.add_field(name="Affected", value=str(affected_bugs(str(new), jira_access)))
        embed.add_field(name="Fixed", value=str(fixed_bugs(str(new), jira_access)))

        content = "Version **{}** has just been created!".format(str(new))
        return embed, content

    # Check for archived versions, if there are we send the embed containing that info.
    archived = archived_version(bot, versions)
    if archived:
        embed.title = str(archived)
        embed.add_field(name="Affected", value=str(affected_bugs(str(archived), jira_access)))
        embed.add_field(name="Fixed", value=str(fixed_bugs(str(archived), jira_access)))
        embed.add_field(name="Released", value=str(archived.released))

        content = "Version **{}** has just been archived!".format(str(archived))
        return embed, content

    # Check for released versions, if there are we send the embed containing that info.
    released = released_version(bot, versions)
    if released:
        embed.title = str(released)
        embed.add_field(name="Affected", value=str(affected_bugs(str(released), jira_access)))
        embed.add_field(name="Fixed", value=str(fixed_bugs(str(released), jira_access)))
        embed.add_field(name="Released", value=str(released.released))

        content = "Version **{}** has just been released!".format(str(released))
        return embed, content

    return None


async def version_update_handler(bot, channel):
    # This will call the update reporter and if there was a version change we will send it to discord.
    update = version_update_reporter(bot)
    if update:
        embed, content = update
        await channel.send(content=content, embed=embed)
