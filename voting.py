# HammerBotPython
# voting.py

from data import discord_letters


def convert_multiple_vote(args):
    poll_list = []
    introduction = ""
    vote = ""
    for i in args:
        if "|" in i:
            vote += i[:-1]
            introduction = f'**Description:** ' + vote + f'\n'
            vote = ""
        elif "&" not in i:
            vote += i + " "
        else:
            vote += i[:-1]
            poll_list.append(vote)
            vote = ""

    poll_list.append(vote)
    poll = ""
    print(introduction)
    for pos, option in enumerate(poll_list):
        poll += discord_letters[pos] + " " + option + "\n"
    return poll, poll_list, introduction
