# HammerBotPython
# utilities module
# data.py

"""
All non sensitive data used in functions is stored here. Sensitive data like the bot token and server IP is stored
in the .env file which is in the gitignore. Final is used to show that the variables are constant, and should not
be changed.
"""

import discord
from typing_extensions import Final

developer_ids: Final[list] = [234257395910443008, 561705204630683648]

coordinate_channel: Final[int] = 690080048375529481
application_channel: Final[int] = 647293235248496644
bulletin_board_channel: Final[int] = 724371678393663569
vote_channel_id: Final[int] = 730396648995422288
fixed_bug_channel_id: Final[int] = 737441217754955836

hammer_guild: Final[int] = 645464470633840651

upvote_emote: Final[int] = 689945780844494848
downvote_emote: Final[int] = 689946011854307381
votent_emote: Final[int] = 701747772461678612

vote_emotes: Final[list] = [upvote_emote, downvote_emote, votent_emote]

vote_role_id: Final[int] = 729381591197024379
tour_giver_id: Final[int] = 702542764893536346
never_alone_id: Final[int] = 770083452581969940
cmp_role_id: Final[int] = 728002223887351830
member_role_id: Final[int] = 645465607856324608
admin_role_id: Final[int] = 649340485093031957

role_ids: Final[dict] = {"tour giver": tour_giver_id,
                         "voten'tn't": vote_role_id,
                         "never-alone": never_alone_id}

role_list: Final[list] = ["tour giver", "voten'tn't"]

hammer_bot_id: Final[int] = 724012480661028907

discord_letters: Final[list] = [
    "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
    "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
    ]

bug_colour_mappings: Final[dict] = {"Open": discord.Color.red(),
                                    "In Progress": discord.Colour.orange(),
                                    "Resolved": discord.Colour.green(),
                                    "Reopened": discord.Colour.blue(),
                                    "Postponed": discord.Colour.purple(),
                                    "Closed": discord.Colour.dark_grey()
                                    }
