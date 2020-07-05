def convert_multiple_vote(arg):
    poll_list = []
    vote = ""
    for i in args:
        if "&" not in i:
            vote += i + " "
        else:
            vote += i[:-1]
            poll_list.append(vote)
            vote = ""

    poll_list.append(vote)
    poll = ""
    for pos, option in enumerate(poll_list):
        poll += discord_letters[pos] + " " + option + "\n"
    return poll, poll_list
