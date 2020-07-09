#HammerBot Python
This repo represents the code for HammerBot that doesn't need to pull data from the Minecraft server. This bot is used on the [HammerSMP Discord Guild](https://discord.gg/QMuwbqa)

The part of the bot that interacts with the server can be found on [AMereBagatelles repository](https://github.com/AMereBagatelle/HammerBot).

This bot has various utilities that get used on the server like voting, todo messages editable by anyone, bulletin boards, applications and more

All code is written to be as easily portable as possible, most guild specific data is in **data.py**.

For any issues or questions you can contact `Viktor40#0001` on discord.
###Coordinate List
This feature lets people add or remove coordinates to a message in a coordinate channel. This is still WIP and will be moved to Embeds.

###Bug reports
When someone posts either a link to a bug report or the code of a bug (e.g MC-190669) and will post an embed containing a summary of the issue containing most of the important info. I used [Grohiik's code for accessing the bug tracker](https://gist.github.com/Grohiik/bc86c86a1536e343304d5bb07c924923).

###Role
The bot has the ability to give members certain roles if they want to. Those are mostly utility roles used for pinging but can be switched out to anything.

The command has the following syntax 
```
/role <action> <role>
```
Possible actions are `add` and `remove` and roles can be configured.

###Bulletin
This command will create a bulletin for a specific task in the bulletin channel where all members can add or remove bulletins.

The command has the following syntax 
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

###todo
This command will create a todo list for a specific project in the project channel. All members can add or remove bulletins, and the todo list will be pinned by the bot.

The command has the following syntax 
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

###Mass Delete
This command will delete the latest messages in a channel. This can be used for moderating. You need to provide the number of messages you want to delete.

The command has the following syntax 
```
/mass_delete <number_of_messages>
```

###Other smaller features
#####User leave notification
This will send a message to the guilds system message channel if the latest person who joined the server left again. This will stop people from welcoming people who left the guild.

#####Test
Tests if the bot is working by sending a little message.
The command has the following syntax 
```
/test
```

#####Stop Lazy
Tells someone to stop being lazy and sends [stop_lazy.png](https://github.com/viktor40/HammerBotPython/blob/master/stop_lazy.png) to discord.
```
/stop_lazy <person="">
```
You can provide an extra argument, and if provided the bot will tell a specific user to stop being lazy.

#####CMP
This command will DM the CMP IP to people with CMP access role
```
/CMP
```
