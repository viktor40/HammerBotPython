from Token import mojira_password, mojira_username, hekate_token as TOKEN
import discord
import re
from jira import JIRA
from discord.utils import get



regex = re.compile(
    "((mc|mcapi|mcce|mcds|mcl|mcpe|realms|sc|web)-[0-9]+)", re.IGNORECASE
)

client = discord.Client()
hekate_movienight = 698390726337232967
hekate_weebcorner = 698966349526859862
hekate_join_log = 720034217920036974


Voicechannel = {}


async def mc_bug(message, issues):
    jira = JIRA(
        server="https://bugs.mojang.com",
        basic_auth=(mojira_username, mojira_password),
    )

    for issueid in issues:
        try:
            issue = jira.issue(issueid[0])

            embed = discord.Embed(
                color=0xA7D9FC,
                title=str.upper(issueid[0]),
                description=f"**{issue.fields.summary}**",
                url=f"https://bugs.mojang.com/browse/{issueid[0]}",
            )
            embed.add_field(name="Status", value=issue.fields.status)
            embed.add_field(name="Resolution", value=issue.fields.resolution)

            embed.set_footer(text=f"created: {issue.fields.created[:10]}")

            await message.channel.send(embed=embed)
        except:
            try:
                await message.channel.send(f"{issueid[0]} does not exist")
            except:
                await message.channel.send(f"fuck off {message.author.mention}")


@client.event
async def on_member_join(member):
    channel = client.get_channel(hekate_join_log)
    await channel.send(f"Member joined: {member.name}")


@client.event
async def on_member_remove(member):
    channel = client.get_channel(hekate_join_log)
    await channel.send(f"{member.name} left us ;-;")


@client.event
async def on_voice_state_update(member, before, after):
    global Voicechannel

    if after.channel and before.channel:
        if (
            after.self_deaf
            and not before.self_deaf
            and before.channel != member.guild.afk_channel
            and before.channel.id != hekate_movienight
            and before.channel.id != hekate_weebcorner
        ):
            await member.move_to(member.guild.afk_channel)
            Voicechannel[member] = before.channel
        elif not after.self_deaf and before.self_deaf and member in Voicechannel:
            await member.move_to(Voicechannel[member])
            Voicechannel.pop(member)
    elif member in Voicechannel:
        Voicechannel.pop(member)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    issues = re.findall(regex, message.content)
    if issues:
        await mc_bug(message, issues)


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


client.run(TOKEN)