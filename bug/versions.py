# HammerBotPython
# bug module
# versions.py

from jira import JIRA
import os
from dotenv import load_dotenv
import discord

load_dotenv()
mojira_username = os.getenv("mojira_username")
mojira_password = os.getenv("mojira_password")


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


def get_from_filter(jira_filter, jira_access):
    filter_list = jira_access.search_issues(jira_filter, maxResults=False)
    filter_len = len(filter_list)
    return filter_len


def affected_bugs(version, jira_access):
    jira_filter = 'project = MC AND affectedVersion = "{}" ORDER BY updated DESC'.format(version)
    number_affected = get_from_filter(jira_filter, jira_access)
    return number_affected


def fixed_bugs(version, jira_access):
    jira_filter = 'project = MC AND fixVersion = "{}" ORDER BY updated DESC'.format(version)
    number_fixes = get_from_filter(jira_filter, jira_access)
    return number_fixes


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


def archived_version(bot, versions):
    previous_version = versions[-2]
    if not bot.previous_version_archive_status and previous_version.archive:
        bot.previous_version_archive_status = previous_version.archive
        return previous_version
    else:
        return None


def released_version(bot, versions):
    latest_version = versions[-1]
    if not bot.latest_version_release_status and latest_version.released:
        bot.latest_version_release_status = latest_version.released
        return latest_version
    else:
        return None


def version_update_reporter(bot):
    jira_access = JIRA(
        server="https://bugs.mojang.com",
        basic_auth=(mojira_username, mojira_password),
    )
    versions = jira_access.project("MC").versions

    embed = discord.Embed(color=discord.Colour.magenta())

    new = new_version(bot, versions)
    if new:
        embed.title = str(new)
        embed.add_field(name="Affected", value=str(affected_bugs(str(new), jira_access)))
        embed.add_field(name="Fixed", value=str(fixed_bugs(str(new), jira_access)))

        content = "Version **{}** has just been created!".format(str(new))
        return embed, content

    archived = archived_version(bot, versions)
    if archived:
        embed.title = str(archived)
        embed.add_field(name="Affected", value=str(affected_bugs(str(archived), jira_access)))
        embed.add_field(name="Fixed", value=str(fixed_bugs(str(archived), jira_access)))
        embed.add_field(name="Released", value=str(archived.released))

        content = "Version **{}** has just been archived!".format(str(archived))
        return embed, content

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
    update = version_update_reporter(bot)
    if update:
        embed, content = update
        await channel.send(content=content, embed=embed)
