from discord.ext import commands

"""
This will later be used for the custom help command. Currently the built in help command is used.
"""


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

        # try and except in case of MissingRole. MissingRole error means the person doesn't have perms to use that.
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
    return command_list


def formatter():
    pass


def helper():
    pass
