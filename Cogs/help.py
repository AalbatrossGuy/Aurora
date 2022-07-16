import discord, json
from discord.ext import commands
from discord import app_commands
from customs.log import AuroraLogger
from customs.help_embeds import embedModeration, embedSettings, embedUtility, embedImage, embedSearch

# LOGGER
error_logger = AuroraLogger("AuroraErrorLog", "logs/errors.log")

# config.json
file = open("config.json", "r")
config = json.loads(file.read())


# VIEW
class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(HelpSelect())
        self.add_item(HelpButton())
        self.add_item(
            discord.ui.Button(label="Invite Me", style=discord.ButtonStyle.url, url=config["METADATA"]["INVITE_LINK"],
                              emoji="<:invite:993158095721201764>"))
        self.add_item(discord.ui.Button(label="Github", style=discord.ButtonStyle.url,
                                        url=f'{config["METADATA"]["GITHUB_REPOSITORY"]}',
                                        emoji="<:link:908297685545656370>"))


class HelpOnlyButtons(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(HelpButton())
        self.add_item(
            discord.ui.Button(label="Invite Me", style=discord.ButtonStyle.url, url=config["METADATA"]["INVITE_LINK"],
                              emoji="<:invite:993158095721201764>"))
        self.add_item(discord.ui.Button(label="Github", style=discord.ButtonStyle.url,
                                        url=f'{config["METADATA"]["GITHUB_REPOSITORY"]}',
                                        emoji="<:link:908297685545656370>"))


# INTERACTIONS
class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Moderation", description="clear, ban, kick, etc.",
                                 emoji="<:mod:992770697921310780>"),
            discord.SelectOption(label="Settings", description="about, etc.", emoji="<:settings:957629477087760436>"),
            discord.SelectOption(label="Utility", description="avatar, meminfo, etc.",
                                 emoji="<:utilitywhat:992784837205311498>"),
            discord.SelectOption(label="Image", description="b_w, negative, etc.", emoji="<:photo:995519248006905896>"),
            discord.SelectOption(label="Search", description="anime, movie, etc.", emoji="<:search:997798789354107030>")
        ]
        super().__init__(placeholder="Select a Help Category", max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0].lower() == "moderation":
            await interaction.response.edit_message(embed=embedModeration)

        if self.values[0].lower() == "settings":
            await interaction.response.edit_message(embed=embedSettings)

        if self.values[0].lower() == "utility":
            await interaction.response.edit_message(embed=embedUtility)

        if self.values[0].lower() == "image":
            await interaction.response.edit_message(embed=embedImage)

        if self.values[0].lower() == "search":
            await interaction.response.edit_message(embed=embedSearch)


class HelpButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🗑️", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        if self.label == "🗑️":
            await interaction.message.delete()


# COMMANDS
class AuroraHelp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="help", description="Shows the help message for the bot.")
    async def _help(self, interaction: discord.Interaction, category: str = None):
        try:
            view = HelpView()
            onlyButtons = HelpOnlyButtons()
            if not category:
                embed = discord.Embed(
                    title="<a:Hello:917378477638946877> Aurora Help", colour=discord.Colour.blurple(),
                    description=f"**Use `/help` or `/help [category]` for seeing this help message or help on a category.\n\nTotal Commands `{len(list(self.client.tree.walk_commands())):,}` | Total members `{len(list(self.client.get_all_members())):,}` | Total Guilds `{len(list(self.client.guilds))}`**",
                    timestamp=interaction.created_at)
                embed.set_thumbnail(url=self.client.user.display_avatar)
                embed.set_footer(text="There are hundreds of documented reports of ‘auroral sound’",
                                 icon_url=interaction.user.display_avatar)

                embed.add_field(name="<:mod:992770697921310780> Moderation", value="`/help moderation`")
                embed.add_field(name="<:settings:957629477087760436> Settings", value="`/help settings`")
                embed.add_field(name="<:utilitywhat:992784837205311498> Utility", value="`/help utility`")
                embed.add_field(name="<:photo:995519248006905896> Image", value="`/help image`")
                embed.add_field(name="<:search:997798789354107030> Search", value="`/help search`")

                await interaction.response.send_message(embed=embed, view=view)

            elif category.lower() == "moderation":
                await interaction.response.send_message(embed=embedModeration, view=onlyButtons)

            elif category.lower() == "settings":
                await interaction.response.send_message(embed=embedSettings, view=onlyButtons)

            elif category.lower() == "utility":
                await interaction.response.send_message(embed=embedUtility, view=onlyButtons)

            elif category.lower() == "image":
                await interaction.response.send_message(embed=embedImage, view=onlyButtons)

            elif category.lower() == "search":
                await interaction.response.send_message(embed=embedSearch, view=onlyButtons)

        except:
            error_logger.error("Error occurred while running help command:- ", exc_info=True)


async def setup(client):
    await client.add_cog(AuroraHelp(client))
