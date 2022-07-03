import discord, json
from discord.ext import commands
from discord import app_commands
from customs.log import AuroraLogger
from customs.help_embeds import embedModeration, embedSettings

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
        self.add_item(discord.ui.Button(label="Invite Me", style=discord.ButtonStyle.url, url=config["METADATA"]["INVITE_LINK"], emoji="<:invite:993158095721201764>"))
        self.add_item(discord.ui.Button(label="Github", style=discord.ButtonStyle.url,
                                        url=f'{config["METADATA"]["GITHUB_REPOSITORY"]}',
                                        emoji="<:link:908297685545656370>"))


# INTERACTIONS
class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Moderation", description="clear, ban, kick, etc.",
                                 emoji="<:mod:992770697921310780>"),
            discord.SelectOption(label="Settings", description="about, etc.", emoji="<:settings:957629477087760436>")
        ]
        super().__init__(placeholder="Select a Help Category", max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0].lower() == "moderation":
            await interaction.response.edit_message(embed=embedModeration)

        if self.values[0].lower() == "settings":
            await interaction.response.edit_message(embed=embedSettings)


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
            if not category:
                embed = discord.Embed(
                    title="<a:Hello:917378477638946877> Aurora Help", colour=discord.Colour.blurple(),
                    description=f"**Use `/help` or `/help [category]` for seeing this help message or help on a category\n\nTotal Commands `{len(list(self.client.tree.walk_commands())):,}` | Total members `{len(list(self.client.get_all_members())):,}` | Total Guilds `{len(list(self.client.guilds))}`**",
                    timestamp=interaction.created_at)
                embed.set_thumbnail(url=self.client.user.display_avatar)
                embed.set_footer(text="There are hundreds of documented reports of ‘auroral sound’",
                                 icon_url=interaction.user.display_avatar)

                embed.add_field(name="<:mod:992770697921310780> Moderation", value="`/help moderation`")
                embed.add_field(name="<:settings:957629477087760436> Settings", value="`/help settings`")
                embed.add_field(name="<:utilitywhat:992784837205311498> Utility", value="`/help utility`")
                embed.add_field(name="<:clown:992786518445932707> Fun", value="`/help fun`")
                view = HelpView()
                await interaction.response.send_message(embed=embed, view=view)

                # await interaction.response.defer(thinking=True)

        except:
            error_logger.error("Error occurred while running help command:- ", exc_info=True)


#
#     @interactions.extension_command(
#         name="help",
#         description="Shows the help message for the bot.",
#         scope=903225083072495646,
#         options=[
#             interactions.Option(
#                 name="category_name",
#                 description="The command whose help message you want to see.",
#                 type=interactions.OptionType.STRING,
#                 required=False,
#             ),
#         ],
#     )
#     async def _help_message(self, ctx: interactions.CommandContext, category_name: str = None):
#         if not category_name:
#             fields = [
#                 interactions.EmbedField(name="<:server:908295956011810816> **General**", value="`ping`, `coming soon...`", inline=True),
#                 interactions.EmbedField(name="<:mod:908289844395016232> **Moderation**", value="`clear`, `kick`, `ban`, `unban`, `coming soon...`", inline=True),
#                 interactions.EmbedField(name="<:settings:957629477087760436> **Settings**", value="`about`, `coming soon...`", inline=True)
#             ]
#             embed = createEmbed(title='AuroraBot Help Message', color=1752220, footer_text="The oldest known record of an aurora dates back to 2600 BC.",
#             footer_icon_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
#             thumbnail_url="https://cdn.discordapp.com/attachments/831369746855362590/955342757361250314/unknown.png",
#             description=f"**Total Commands: `{len(await self.client._http.get_application_commands(self.client.me.id, 903225083072495646))}`**\nDo /help [category] to get more info about a category.",
#             author_name="AalbatrossGuy#5129", author_icon_url="https://media.discordapp.net/attachments/831369746855362590/898903606319800340/IMG_20211009_172918_418.jpg", fields=fields)
#             await ctx.send(embeds=embed)
#
#         elif category_name.lower() == 'general':
#             fields = [
#                 interactions.EmbedField(name="📌 ping", value="*↳ Shows the Bot's latency*"),
#             ]
#             embed = createEmbed(title='Aurora Help Message : General', color=1752220, footer_text="The aurora borealis feature in Norse mythology.",
#                 footer_icon_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
#                 thumbnail_url="https://cdn.discordapp.com/attachments/831369746855362590/955338534737313792/unknown.png",
#                 description="Help Regarding The `General` Category.",
#                 fields=fields
#             )
#             await ctx.send(embeds=embed)
#
#         elif category_name.lower() == 'moderation':
#             fields = [
#                 interactions.EmbedField(name="📌 clear [amount(Optional)]", value="*↳ The [amount] of messages to delete from the channel.*"),
#                 interactions.EmbedField(name="📌 kick [member][reason(Optional)]", value="*↳ The [member] to kick from the server for [reason].*"),
#                 interactions.EmbedField(name="📌 ban [member][reason(Optional)]", value="*↳ The [member] to ban from the server for [reason].*"),
#                 interactions.EmbedField(name="📌 unban [member_id]", value="*↳ The [member_id] to unban from the server for [reason].*")
#             ]
#             embed=createEmbed(title="Aurora Help Message : Moderation", color=1752220, footer_text="The aurora borealis play a part in Chinese dragon legends",
#                 footer_icon_url = "https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
#                 thumbnail_url="https://cdn.discordapp.com/attachments/831369746855362590/955340786948505600/unknown.png",
#                 description="Help Regarding The `Moderation` Category.",
#                 fields=fields
#             )
#             await ctx.send(embeds=embed)
#
#         elif category_name.lower() == 'settings':
#             fields = [
#                 interactions.EmbedField(name="📌 about", value="*↳ Displays information about the bot.*"),
#             ]
#             embed=createEmbed(title="Aurora Help Message : Settings", color=1752220, footer_text="The term ‘aurora borealis’ was coined in 1619",
#                 footer_icon_url = "https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
#                 thumbnail_url="https://cdn.discordapp.com/attachments/831369746855362590/957630340330037258/unknown.png",
#                 description="Help Regarding The `Moderation` Category.",
#                 fields=fields
#             )
#             await ctx.send(embeds=embed)
#
async def setup(client):
    await client.add_cog(AuroraHelp(client))
