# HammerBotPython
# data.py

import discord

coordinate_channel = 690080048375529481
application_channel = 647293235248496644
bulletin_board_channel = 724371678393663569

hammer_guild = 645464470633840651

upvote_emote = 689945780844494848
downvote_emote = 689946011854307381
votent_emote = 701747772461678612

vote_emotes = [upvote_emote, downvote_emote, votent_emote]

vote_role_id = 729381591197024379
tour_giver_id = 702542764893536346

role_ids = {"tour giver": vote_role_id, "voting": tour_giver_id}
role_list = ["tour giver", "voten'tn't"]

hammer_bot_id = 724012480661028907

discord_letters = [
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

bug_colour_mappings = {"Open": discord.Color.red(),
                       "In Progress": discord.Colour.orange(),
                       "Resolved": discord.Colour.green(),
                       "Reopened": discord.Colour.blue(),
                       "Postponed": discord.Colour.purple(),
                       "Closed": discord.Colour.dark_grey()}