from utilities.data import role_list

# general syntax
syntax_pre = "The command has the following syntax:\n"

# ping command
ping_usage = f"This command will tell you if the bot is online."
ping_help = f"This command will tell you if the bot is online.\n" \
            f"It will also tell you the ping and the socket response time." \
            f"{syntax_pre}`/ping`"

# testing command
testing_usage = f"This command is purely for testing purposes, don't use it"
testing_help = f"This command is purely for testing purposes, don't use it.\n" \
               f"Syntax and usage are highly variable."

# role command
role_usage = f"This command will give you the ability to add or remove certain roles."
role_help = f"{role_usage}\n\n{syntax_pre}" \
            f"/role <action> [role]\n" \
            f"The different actions are:\n" \
            f"  - `list`: This will give you a list of available roles.\n\n" \
            f"  - `add`: This will add a role to your user.\n\n" \
            f"  - `remove`: This will remove a role from your user.\n\n" \
            f"The available roles are: {', '.join(role_list)}"

# stop_lazy command
stop_lazy_usage = f"This command will tell someone to stop lazy."
stop_lazy_help = f"{stop_lazy_usage}\n\n{syntax_pre}" \
                 f"`/stop_lazy {'{person=None}'}` where person is an option argument."

# CMP command
CMP_usage = f"This command is able to give anyone with CMP access role the IP."
CMP_help = f"{CMP_usage}\n\n{syntax_pre}" \
           f"`/CMP`\n" \
           f"The command will send the IP via DM."

# vote command
vote_usage = f"This command can be used to create polls in the voting channel."
vote_help = f"{vote_usage}\n\n{syntax_pre}" \
            f"`/vote <vote_type> <*args>`\n" \
            f"Vote type can be one of the following:\n" \
            f"  - `yes_no`: This will create a poll with only the option to vote yes, no or abstain.\n" \
            f"          specific syntax: `/vote yes_no <something to vote on>`\n\n" \
            f"  - `multiple`: This will create a poll where you can have multiple options, A - Z.\n" \
            f"          specific syntax: `/vote multiple <something to vote on> | <option 1> & <option 2> ...`\n\n" \
            f"  - `close`: This will close a poll after voting is done.\n" \
            f"          specific syntax: `/vote close <vote title>`\n\n" \
            f"  - `reopen`: This will reopen the poll in case that's necessary.\n" \
            f"          specific syntax: `/vote reopen <vote title>`\n\n" \
            f"The `<vote title>` is always the title of the embed (in bold at the top underneath the author)."

# bulletin command
bulletin_usage = f"This command will provide a way to create, edit and remove bulletins on the bulletin board."
bulletin_help = f"{bulletin_usage}\n\n{syntax_pre}" \
                f"`/bulletin <action> <*args>`" \
                f"Possible actions are:\n" \
                f"  - `create`: Create a new board for a project.\n" \
                f"          specific syntax: `/bulletin create <project name> | <first task> & <second task> ...`\n\n" \
                f"  - `add`: Add a bulletin to a specific board\n" \
                f"          specific syntax: `/bulletin add <project name> | <extra task> & <extra task> ...`\n\n" \
                f"  - `remove`: Remove a bulletin from a specific board.\n" \
                f"          specific syntax: `/bulletin remove <project name> | <task> & <task> ...`\n\n" \
                f"  - `delete`: Delete a board entirely\n" \
                f"          specific syntax: `/bulletin remove <project name>`\n\n" \
                f"The `<project name>` is always the title of the embed (in bold at the top of the embed)."

# to do command
todo_usage = f"This command will provide a way to create, edit and remove todo list in the pinned messages."
todo_help = f"{todo_usage}\n\n{syntax_pre}" \
            f"`/todo <action> <*args>`" \
            f"Possible actions are:\n" \
            f"  - `create`: Create a new board for a project.\n" \
            f"          specific syntax: `/todo create <project name> | <first task> & <second task> ...`\n\n" \
            f"  - `add`: Add a bulletin to a specific board\n" \
            f"          specific syntax: `/todo add <project name> | <extra task> & <extra task> ...`\n\n" \
            f"  - `remove`: Remove a bulletin from a specific board.\n" \
            f"          specific syntax: `/todo remove <todo name> | <task> & <task> ...`\n\n" \
            f"  - `delete`: Delete a board entirely\n" \
            f"          specific syntax: `/todo remove <todo name>`\n\n" \
            f"The `<todo name>` is always the title of the embed (in bold at the top of the embed).\n" \
            f"The message will be pinned automatically by the bot."

# coordinates command
coordinates_usage = f"This command will provide a way to create, edit and remove coordinates to the coordinate list."
coordinates_help = f"{todo_usage}\n\n{syntax_pre}" \
                   f"`/coordinate <action> <*args>`" \
                   f"Possible actions are:\n" \
                   f"  - `create`: Create a new board for a project.\n" \
                   f"          specific syntax: `/coordinate create <dimension> | <first coord> & <second coord> ...`\n\n" \
                   f"  - `add`: Add a bulletin to a specific board\n" \
                   f"          specific syntax: `/coordinate add <dimension> | <extra coord> & <extra coord> ...`\n\n" \
                   f"  - `remove`: Remove a bulletin from a specific board.\n" \
                   f"          specific syntax: `/coordinate remove <dimension> | <coord> & <coord> ...`\n\n" \
                   f"  - `delete`: Delete a board entirely\n" \
                   f"          specific syntax: `/coordinate remove <dimension>`\n\n" \
                   f"The `<dimension>` is always the title of the embed (in bold at the top of the embed).\n" \
                   f"There is currently still the possibility to create or delete dimension boards." \
                   f"This is done because the system does not yet provide a way to handle lists that are longer" \
                   f"than the embed character limit. Use this wisely. If a list reaches the limit, create a new list" \
                   f"of that dimension and add a index number after it."

# mass_delete command
mass_delete_usage = f"This command will provide admins a way to mass delete messages"
mass_delete_help = f"{mass_delete_usage}\n\n{syntax_pre}" \
                   f"`/mass_delete <number of messages`\n" \
                   f"`<number of messages` cannot be bigger than 200.\n" \
                   f"This command can only be used by admins."

# help command
help_usage = f"Shows this command."
help_help = f"Shows the help command. By giving the command an extra argument you can get " \
            f"more specific help on a certain command.\n\n{syntax_pre}" \
            f"/help {'{command=None}'}"

# other bot functions
other_usage = f"This will provide a list of other functions that the bot has that are not command based."
other_help = f"This is a list of other functions that the bot has that are not related to commands.\n" \
             f"  - Tracking of the latest person who joined the discord and sending a message in #spam" \
             f"if they left soon after joining so people don't accidentally o/.\n\n" \
             f"  - Other server related stuff that needs to be added to the command soon.\n\n" \
             f"  - Other features that will come soontm"

# HammerBot java commands:

# online command
online_usage = f"See who is online on a certain server."
online_help = f"{online_usage}\n\n{syntax_pre}" \
              f"`/online <server>`\n" \
              f"The server can either be `SMP`, `CMPCOPY` or `CMPFLAT`"

# whitelist command
whitelist_usage = f"Whitelist a player on a certain server"
whitelist_help = f"{whitelist_usage}\n\n{syntax_pre}" \
                 f"`/whitelist <server> <player name>`\n" \
                 f"The server can either be `SMP`, `CMPCOPY` or `CMPFLAT`\n\n" \
                 f"This command is admin only"

# scoreboard command
scoreboard_usage = f"Show a scoreboard from the server in discord [Currently not working]"
scoreboard_help = f"{scoreboard_usage}"

# uploadFile command
upload_file_usage = f"Upload a file to the server."
upload_file_help = f"{upload_file_usage}\n\n{syntax_pre}" \
                   f"`/upload <file>`\n\n" \
                   f"The file can either be a structure file or a scarpet file."
