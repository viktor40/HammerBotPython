# HammerBotPython
# help_command module
# helping.py

from discord.ext import commands
import discord
from help_command.help_data import other_usage, other_help, bug_usage, bug_help


# this command will go through all commands, fetch the name, usage and help variable given to the
# discord.ext.commands.Bot.command decorator and pass the context to checks to see if the sender has permissions
# to use that command
def permissions(ctx, bot):
    command_list = {}
    # iterate over all commands
    for com in bot.commands:
        # register name, usage and help
        name = com.name
        usage = com.usage
        help_text = com.help

        # try and except in case of MissingRole. MissingRole error means the person doesn't have perms to use that.q
        try:
            check = com.checks
            # check if the command actually has any checks (public commands don't for instance)
            # if there are no checks it will always be possible to use the command, so it's always true
            if check:
                permitted = com.checks[0](ctx)
                command_list[name] = (usage, help_text, permitted)
            else:
                permitted = True
                command_list[name] = (usage, help_text, permitted)
        except commands.MissingRole:
            permitted = False
            command_list[name] = (usage, help_text, permitted)

    # add things to help that are either from HammerBot Java or not based on commands
    command_list["other"] = (other_usage, other_help, True)
    command_list["bug"] = (bug_usage, bug_help, True)

    # sort the commands in the dictionary on the keys (command names)
    sorted_key = sorted(command_list.keys(), key=lambda x: x.lower())
    return sorted_key, command_list


# formatting of the help command
def help_formatter(ctx, bot):
    help_embed = discord.Embed(
        color=discord.Color.orange(),
        title="HammerBot Help",
        description="Use `/help <command>` to get a more in depth information on a command."
    )

    # get the list of all the help stuff and iterate over the sorted keys so it's in alphabetical order
    sorted_key, command_list = permissions(ctx, bot)
    for name in sorted_key:
        usage, help_text, permitted = command_list[name]
        # this will check if the person has the right perms to use the command, if not it won't show help for it
        if permitted:
            help_embed.add_field(name=name, value=usage, inline=False)
    return help_embed


# this function is used for the command specific help commands which you can bring up by using /help <command>
def help_verbose(ctx, bot, argument):
    command_list = permissions(ctx, bot)[1]
    help_text = command_list[argument][1]
    permitted = command_list[argument][2]

    help_embed = discord.Embed(
        color=discord.Color.orange(),
        title="HammerBot Help on the {} command".format(argument),
    )
    if permitted:
        help_embed.description = help_text
    else:
        help_embed.description = "You don't have perissions to use this command."

    return help_embed


def helper(ctx, bot, argument):
    if argument:
        help_embed = help_verbose(ctx, bot, argument)

    else:
        help_embed = help_formatter(ctx, bot)

    return help_embed
