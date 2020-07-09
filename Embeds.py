import discord


class RichEmbed:
    def __init__(self, color="", title="", description="", url="", author="", author_icon="", footer="", fields=None):
        self.color = color
        self.title = title
        self.description = description
        self.url = url
        self.author = author
        self.author_icon = author_icon
        self.footer = footer
        self.fields = fields

    def get_embed(self):
        embed = discord.Embed()
        if self.color:
            embed.colour = self.color

        if self.title:
            embed.title = self.title

        if self.description:
            embed.description = self.description

        if self.url:
            embed.url = self.url

        if self.author:
            if self.author_icon:
                embed.set_author(name=self.author, url=self.author_icon)
            else:
                embed.set_author(name=self.author)

        if self.footer:
            embed.set_footer(text=self.footer)

        if self.fields:
            for name in self.fields:
                embed.add_field(name=name, value=self.fields[name])

        return embed

    def __len__(self):
        fields_len = 0
        for name in self.fields:
            fields_len += len(name) + len(self.fields[name])
        return len(self.title) + len(self.description) + len(self.url) + len(self.author) + len(self.footer) + fields_len


class TaskEmbed(RichEmbed):
    def __init__(self, project, formatted, channel_history, color="", title="", description="", url="", author=""
                 , author_icon="", footer="", fields=None):
        super(TaskEmbed, self).__init__(self, color=color, title=title, description=description, url=url,
                                        author=author, author_icon=author_icon, footer=footer, fields=fields)
        self.project = project
        self.formatted = formatted
        self.channel_history = channel_history

    def create_task_embed(self):
        embed = discord.Embed(
            color=self.color,
            title=self.project,
            description=self.formatted
        )
        return embed

    def __add__(self, other):
        if self.project[:-1] == " ":
            project = self.project[:-1]
        for message in self.channel_history:
            if message.embeds:
                if message.embeds[0].title == project:
                    edited_embed = discord.Embed(
                        color=0xe74c3c,
                        title=message.embeds[0].title,
                        description=message.embeds[0].description + "\n" + formatted
                    )
                    return message, edited_embed
