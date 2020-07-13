# HammerBotPython
# bug.py

import discord
from jira import JIRA
import re
from dotenv import load_dotenv  # load module for usage of a .env file (pip install python-dotenv)
import os  # import module for directory management

load_dotenv()  # load the .env file containing id's that have to be kept secret for security
mojira_username = os.getenv("mojira_username")
mojira_password = os.getenv("mojira_password")

regex = re.compile("(png|jpg|jpeg)")
valid = re.findall(regex, "https://bugs.mojang.com/secure/attachment/294180/2020-05-09_10.59.39.png")
print(valid)
