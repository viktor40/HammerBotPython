# HammerBot Python
This repo represents the code for HammerBot that doesn't need to pull data from the Minecraft server. This bot is used on the [HammerSMP Discord Guild](https://discord.gg/QMuwbqa)

The part of the bot that interacts with the server can be found on [AMereBagatelles repository](https://github.com/AMereBagatelle/HammerBot).

This bot has various utilities that get used on the server like voting, todo messages editable by anyone, bulletin boards, applications and more

All code is written to be as easily portable as possible, most guild specific data is in `utilities.data.py`.

For any issues or questions you can contact `Viktor40#0001` on discord.
### Coordinate List
This feature lets people add or remove coordinates to a message in a coordinate channel.
There are supposed to be 3 embeds, one for each dimension (overworld, nether, end). People can add or remove locations to this.

The command has the following syntax:
```
/coordinate <action> <*args>
```
Possible actions are: `create`, `add`, `remove` and `delete`

**Some examples:**

Create a new bulletin with tasks
`/coordinate create <dimension> | <first coordinate> & <second coordinate> & <third coordinate> ...`

Add a bulletin to an existing board:
`/coordinate add <dimension> | <first extra coordinate> & <second extra coordinate> ...`

Remove a bulletin from an existing board, if the last bulletin is removed, the board gets deleted:
`/coordinate remove <dimension> | <first coordinate> & <second coordinate> ...`

Delete a dimension
`/coordinate remove <dimension>`

Currently you can remove and add dimensions. This is because the bot doesn't automatically create a new embed when the character limit has been reached. this will be changed in the future. 

### Role
The bot has the ability to give members certain roles if they want to. Those are mostly utility roles used for pinging but can be switched out to anything.

The command has the following syntax 
```
/role <action> <role>
```
Possible actions are `add` and `remove` and roles can be configured.

### Voting
The bot contains a command that will handle voting. This will be done within an embed. The embed has the thing to vote on as a title and shows the person who created the vote, together with his discord profile picture as the author.
Voting emotes will also be added by the bot so people just have to click on them

The command has the following syntax:
```
/vote <vote_type> <*args>
```
Possible vote types are: `yes_no` and `multiple`

The `yes_no` type will create a vote where people can only vote yes, no or abstain / unsure. The `multiple` vote will give people the ability to add multiple options to the vote. The max amount of options is 26, the amount ot letters in the alphabet.
The different options will be displayed in a nice fashion in the order that the creator listed them in.

**Some examples:**
Create a `yes_no` vote:
`/vote yes_no <something to vote on>`

Create a `multiple` vote:
`/vote multiple <something to vote on> | <option 1>, <option 2> ... <option 26>`

### Bulletin
This command will create a bulletin for a specific task in the bulletin channel where all members can add or remove bulletins.

The command has the following syntax:
```
/buletin <action> <*args>
```
Possible actions are: `create`, `add`, `remove` and `delete`

**Some examples:**

Create a new bulletin with tasks
`/bulletin create <project name> | <first task> & <second task> & <third task> ...`

Add a bulletin to an existing board:
`/bulletin add <project name> | <first extra task> & <second extra task> ...`

Remove a bulletin from an existing board, if the last bulletin is removed, the board gets deleted:
`/bulletin remove <project name> | <first completed task> & <second completed task> ...`


Delete a board
`/bulletin remove <project name>`

### todo
This command will create a todo list for a specific project in the project channel. All members can add or remove bulletins, and the todo list will be pinned by the bot.

The command has the following syntax:
```
/todo <action> <*args>
```
Possible actions are: `create`, `add`, `remove` and `delete`

**Some examples:**

Create a new bulletin with tasks
`/todo create <project name> | <first task> & <second task> & <third task> ...`

Add a bulletin to an existing board:
`/todo add <project name> | <first extra task> & <second extra task> ...`

Remove a bulletin from an existing board, if the last bulletin is removed, the board gets deleted:
`/todo remove <project name> | <first completed task> & <second completed task> ...`

Delete a board
`/todo remove <project name>`

### Mass Delete
This command will delete the latest messages in a channel. This can be used for moderating. You need to provide the number of messages you want to delete.

The command has the following syntax:
```
/mass_delete <number_of_messages>
```

### Bug report handling
##### Show bug reports:
When someone posts either a link to a bug report or the code of a bug (e.g MC-190669) and will post an embed containing a summary of the issue containing most of the important info. I used [Grohiik's code for accessing the bug tracker](https://gist.github.com/Grohiik/bc86c86a1536e343304d5bb07c924923).
Custom code was used for everything other than accessing the jira API

The different types of bugs are:
`mc`, `mcapi`, `mcce`, `mcd`, `mcl`, `mcpe`, `mce`, `realms`, `web`, `bds`

An example is: mc-69. It is not case sensitive.
The following is a list of what the different abbreviations mean:
- `mc`: Minecraft Java Edition
- `mcapi`: Minecraft API
- `mcce`: Minecraft Console Edition
- `mcd`: Minecraft Dungeons
- `mcl`: Minecraft Launcher
- `mcpe`: Minecraft (Bedrock Codebase)
- `mce`: Minecraft Earth
- `realms`: Minecraft Realms
- `web`: Mojang Web Services
- `bds`: Bedrock Dedicated Server

##### Bug resolution checker
This will check if bugs have been resolved as fixed or as won't fix and puts them in a predefined channel.

##### New version checker
This will check weather a new version has been added on the bug tracker, when it is released and when a older version is archived.

On each of these events the bot will send an embed showing how many bugs were fixed in that version and how many bugs the version affected.

### Custom help command
A custom help command is used. When someone uses `/help` it will show all commands that person can use and a small bit of info on them in a nice embed.

When someone uses `/help <command>` it will show a detailed explanation of how the command works as well as it's syntax.

This will only display commands that the user who uses the command can use. It will send an error when it tries to access a command it cannot use.ou 


### Other smaller features
##### User leave notification
This will send a message to the guilds system message channel if the latest person who joined the server left again. This will stop people from welcoming people who left the guild.

##### ping
Tests if the bot is working by sending a little message.
The command has the following syntax 
```
/ping
```

##### Stop Lazy
Tells someone to stop being lazy and sends [stop_lazy.png](https://github.com/viktor40/HammerBotPython/blob/master/stop_lazy.png) to discord.
```
/stop_lazy <person="">
```
You can provide an extra argument, and if provided the bot will tell a specific user to stop being lazy.

##### CMP
This command will DM the CMP IP to people with CMP access role
```
/CMP
```

### Future features
##### Automatic applications and ticket
Check a google form and send new applications to discord as well as automatically creating a ticket for that application.

##### Better in discord handling
We will handle some events via reactions instead of via commands
