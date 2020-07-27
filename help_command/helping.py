from discord.ext import commands

"""
This will later be used for the custom help command. Currently the built in help command is used.
"""


def permissions(ctx, bot):
    command_list = {}
    for com in bot.commands:
        name = com.name
        usage = com.usage
        help_text = com.help
        try:
            check = com.checks
            if check:
                permitted = com.checks[0](ctx)
                command_list[name] = (usage, help_text, permitted)
            else:
                permitted = True
                command_list[name] = (usage, help_text, permitted)
        except commands.MissingRole:
            permitted = False
            command_list[name] = (usage, help_text, permitted)
    return command_list


def formatter():
    pass


def helper():
    pass
