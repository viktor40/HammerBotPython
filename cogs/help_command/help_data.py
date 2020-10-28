# HammerBotPython
# help_command module
# help_data.py

"""
This file contains all the data for the help command.
It has a usage and a help text for each command and some things that aren't commands.
The usage is a small concise explanation of what the command does.
The help is a verbose explanation, containing all the info you need as well as the correct syntax and some examples.
"""

from typing_extensions import Final

from utilities.data import role_list

# general syntax
syntax_pre: Final[str] = "The command has the following syntax:\n"

# ping command
ping_usage: Final[str] = f"This command will tell you if the bot is online."
ping_help: Final[str] = f"This command will tell you if the bot is online.\n" \
                        f"It will also tell you the ping and the socket response time." \
                        f"{syntax_pre}`/ping`"

# testing command
testing_usage: Final[str] = f"This command is purely for testing purposes, don't use it"
testing_help: Final[str] = f"This command is purely for testing purposes, don't use it.\n" \
                           f"Syntax and usage are highly variable."

# role command
role_usage: Final[str] = f"This command will give you the ability to add or remove certain roles."
role_help: Final[str] = f"{role_usage}\n\n{syntax_pre}" \
                        f"/role <action> [role]\n" \
                        f"The different actions are:\n" \
                        f"  - `list`: This will give you a list of available roles.\n\n" \
                        f"  - `add`: This will add a role to your user.\n\n" \
                        f"  - `remove`: This will remove a role from your user.\n\n" \
                        f"The available roles are: {', '.join(role_list)}"

# stop_lazy command
stop_lazy_usage: Final[str] = f"This command will tell someone to stop lazy."
stop_lazy_help: Final[str] = f"{stop_lazy_usage}\n\n{syntax_pre}" \
                             f"`/stop_lazy {'{person=None}'}` where person is an optional argument."

# CMP command
CMP_usage: Final[str] = f"This command is able to give anyone with CMP access role the IP."
CMP_help: Final[str] = f"{CMP_usage}\n\n{syntax_pre}" \
                       f"`/CMP`\n" \
                       f"The command will send the IP via DM."

# vote command
vote_usage: Final[str] = f"This command can be used to create polls in the voting channel."
vote_help: Final[str] = f"{vote_usage}\n\n{syntax_pre}" \
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
bulletin_usage: Final[str] = f"This command will provide a way to create, edit and remove bulletins on the bulletin board."
bulletin_help: Final[str] = f"{bulletin_usage}\n\n{syntax_pre}" \
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
todo_usage: Final[str] = f"This command will provide a way to create, edit and remove todo list in the pinned messages."
todo_help: Final[str] = f"{todo_usage}\n\n{syntax_pre}" \
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
coordinates_usage: Final[str] = f"This command will provide a way to create, edit and remove coordinates to the coordinate list."
coordinates_help: Final[str] = f"{todo_usage}\n\n{syntax_pre}" \
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
mass_delete_usage: Final[str] = f"This command will provide admins a way to purge messages"
mass_delete_help: Final[str] = f"{mass_delete_usage}\n\n{syntax_pre}" \
                               f"`/mass_delete <number of messages`\n" \
                               f"`<number of messages>` cannot be bigger than 250.\n" \
                               f"This command can only be used by admins."

# mini_delete command
mini_delete_usage: Final[str] = f"This command will provide members a way to purge messages"
mini_delete_help: Final[str] = f"{mass_delete_usage}\n\n{syntax_pre}" \
                               f"`/mass_delete <number of messages`\n" \
                               f"`<number of messages>` cannot be bigger than 10.\n" \

# help command
help_usage: Final[str] = f"Shows this command."
help_help: Final[str] = f"Shows the help command. By giving the command an extra argument you can get " \
                        f"more specific help on a certain command.\n\n{syntax_pre}" \
                        f"/help {'{command=None}'}"

# other bot functions
other_usage: Final[str] = f"This will provide a list of other functions that the bot has that are not command based."
other_help: Final[str] = f"This is a list of other functions that the bot has that are not related to commands.\n" \
                         f"  - Tracking of the latest person who joined the discord and sending a message in #spam" \
                         f"if they left soon after joining so people don't accidentally o/.\n\n" \
                         f"  - Minecraft bug display, see `/help bug`\n\n" \
                         f"  - Other features that will come soontm"

# other bot functions
bug_usage: Final[str] = f"This is not a command but rather a listener to handle the display of Minecraft bugs."
bug_help: Final[str] = f"{bug_usage}\n\n{syntax_pre}" \
                       f"This command will look for any instance of a bug being put in a message. " \
                       f"An escape character can be added before the bug to not show the embed." \
                       f"This character is: `%`.\n\n" \
                       f"The different types of bugs are:\n" \
                       f"`mc`, `mcapi`, `mcce`, `mcd`, `mcl`, `mcpe`, `mce`, `realms`, `web`, `bds`\n\n" \
                       f"An example is: mc-69. It is not case sensitive.\n\n" \
                       f"The following is a list of what the different abbreviations mean:\n" \
                       f"- mc: Minecraft Java Edition\n" \
                       f"- `mcapi`: Minecraft API\n" \
                       f"- `mcce`: Minecraft Console Edition\n" \
                       f"- `mcd`: Minecraft Dungeons\n" \
                       f"- `mcl`: Minecraft Launcher\n" \
                       f"- `mcpe`: Minecraft (Bedrock Codebase)\n" \
                       f"- `mce`: Minecraft Earth\n" \
                       f"- `realms`: Minecraft Realms\n" \
                       f"- `web`: Mojang Web Services\n" \
                       f"- `bds`: Bedrock Dedicated Server\n"


bug_vote_usage: Final[str] = f"This command will add a vote to a certain issue on the bug tracker."
bug_vote_help: Final[str] = f"{bug_usage}\n\n{syntax_pre}" \
                            f"`/bug_vote <issue>`" \

disable_usage: Final[str] = f"This command can turn the bot off. Enable it again with `/enable`"
disable_help: Final[str] = f"{bug_usage}\n\n{syntax_pre}" \
                           f"`/disable`\n\n" \
                           f"This command can only be used by the bot developers or the admins. Currently it is only" \
                           f"implemented in HammerBotPython.\n" \
                           f"This command will prevent the bot from doing anything except for enabling itself.\n" \
                           f"To enable the bot again you can simply use `/enable` and everything will work again."

enable_usage: Final[str] = f"This command can turn the bot on again after disabling it with `/disable`."
enable_help: Final[str] = f"{bug_usage}\n\n{syntax_pre}" \
                          f"`/enable`\n\n" \
                          f"This command can only be used by the bot developers or the admins. Currently it is only" \
                          f"implemented in HammerBotPython.\n" \
                          f"This command will make the bot work again after disabling it."


status_usage: Final[str] = f"This command will tell you if the Python bot is currently enabled or disabled."
status_help: Final[str] = f"{bug_usage}\n\n{syntax_pre}" \
                          f"`/status`\n\n" \
                          f"Enabling or disabling the bot is only available to admins and the bot developers." \
                          f"Ask them for more information if you're unsure if the bot needs to be disabled."


chess_usage: Final[str] = f"This command allows you to play chess."
chess_help: Final[str] = f"{chess_usage}\n\n{syntax_pre}" \
                         f"`/hangman <action> <move=''>`\n\n" \
                         f"Possible actions are:\n" \
                         f"- `play`: Create a new chess game and board.\n" \
                         f"- `move`: Move a piece. Example: `/chess move <piece pos><move to>`\n" \
                         f"Example: `/chess move d2d3`\n" \
                         f"- `promote` Promote a piece. Example: `/chess move <move> <piece>`\n" \
                         f"- `checkmate`: Check if there is a checkmate.\n" \
                         f"- `stalemate`: Check if there is a stalemate.\n" \
                         f"- `draw`: Check if the requirements are satisfied to claim a draw.\n\n" \
                         f"The bot will aslo prevent you from using illegal moves.\n" \
                         f"This only supports 1 player at the moment."

hangman_usage: Final[str] = f"This command allows you to play hangman."
hangman_help: Final[str] = f"{hangman_usage}\n\n{syntax_pre}" \
                           f"`/hangman <action> <guess=''>`\n\n" \
                           f"Possible actions are:\n" \
                           f"- `play`: Start a new game.\n" \
                           f"- `stop`: Stop the current game.\n" \
                           f"- `guess`: Guess either a letter or a word.\n\n" \
                           f"The bot will check for duplicate guesses and always tell you the amount of tries left\n" \
                           f"It will also show a character art hangman and a representation of the word completion."

minesweeper_usage: Final[str] = f"This command allows you to play hangman."
minesweeper_help: Final[str] = f"{hangman_usage}\n\n{syntax_pre}" \
                               f"`/minesweeper <difficulty> <size>`\n" \
                               f"Their are 4 difficulties: `easy`, `medium`, `hard`, `extreme`.\n" \
                               f"The size must be in the format: '<xSize>x<ySize>'. A side can not be" \
                               f"larger than 20 and the total number of tiles must be smaller than 190.\n" \
                               f"If no extra values are provided the command defaults to: `/minesweeper medium 10x15."

count_usage: Final[str] = f"Shows the number of members the discord has."
count_help: Final[str] = f"{count_usage}\n\n{syntax_pre}" \
                         f"`/count <optional_arg>`\n" \
                         f"If the optional argument `roles` is provided, the member count per role will be shown, else" \
                         f"the total server member count."


# HammerBot java commands:

# online command
online_usage: Final[str] = f"See who is online on a certain server."
online_help: Final[str] = f"{online_usage}\n\n{syntax_pre}" \
                          f"`/online <server>`\n" \
                          f"The server can either be `SMP`, `CMPCOPY` or `CMPFLAT`"

# whitelist command
whitelist_usage: Final[str] = f"Whitelist a player on a certain server"
whitelist_help: Final[str] = f"{whitelist_usage}\n\n{syntax_pre}" \
                             f"`/whitelist <server> <player name>`\n" \
                             f"The server can either be `SMP`, `CMPCOPY` or `CMPFLAT`\n\n" \
                             f"This command is admin only"

# scoreboard command
scoreboard_usage: Final[str] = f"Show a scoreboard from the server in discord [Currently not working]"
scoreboard_help: Final[str] = f"{scoreboard_usage}"

# uploadFile command
upload_file_usage: Final[str] = f"Upload a file to the server."
upload_file_help: Final[str] = f"{upload_file_usage}\n\n{syntax_pre}" \
                               f"`/upload <file>`\n\n" \
                               f"The file can either be a structure file or a scarpet file."
