import interactions, logging
from datetime import datetime
from customs.customs import AuroraLogger, createEmbed

# LOG SETTINGS
logger = AuroraLogger('AuroraLog', 'logs/info.log')
error_logger = AuroraLogger('AuroraErrorLog', 'logs/errors.log')


# COMMANDS
class AuroraHelp(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.extension_command(
        name="help",
        description="Shows the help message for the bot.",
        scope=903225083072495646,
        options=[
            interactions.Option(
                name="category_name",
                description="The command whose help message you want to see.",
                type=interactions.OptionType.STRING,
                required=False,
            ),
        ],
    )
    async def _help_message(self, ctx: interactions.CommandContext, category_name: str = None):
        if not category_name:
            fields = [
                interactions.EmbedField(name="<:server:908295956011810816> **General**", value="`ping`, `coming soon...`", inline=True),
                interactions.EmbedField(name="<:mod:908289844395016232> **Moderation**", value="`clear`, `kick`, `ban`, `unban`, `coming soon...`", inline=True),
            ]
            embed = createEmbed(title='AuroraBot Help Message', color=1752220, footer_text="The oldest known record of an aurora date back to 2600 BC",
            footer_icon_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
            thumbnail_url="https://cdn.discordapp.com/attachments/831369746855362590/955342757361250314/unknown.png",
            description=f"**Total Commands: `{len(await self.client._http.get_application_commands(self.client.me.id, 903225083072495646))}`**\nDo /help [category] to get more info about a category.",
            author_name="AalbatrossGuy#5129", author_icon_url="https://media.discordapp.net/attachments/831369746855362590/898903606319800340/IMG_20211009_172918_418.jpg", fields=fields)
            await ctx.send(embeds=embed)

        elif category_name.lower() == 'general':
            fields = [
                interactions.EmbedField(name="📌 ping", value="*↳ Shows the Bot's latency*"),
            ]
            embed = createEmbed(title='Aurora Help Message : General', color=1752220, footer_text="The aurora borealis feature in Norse mythology.",
                footer_icon_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
                thumbnail_url="https://cdn.discordapp.com/attachments/831369746855362590/955338534737313792/unknown.png",
                description="Help Regarding The `General` Category.",
                fields=fields
            )
            await ctx.send(embeds=embed)

        elif category_name.lower() == 'moderation':
            fields = [
                interactions.EmbedField(name="📌 clear [amount(Optional)]", value="*↳ The [amount] of messages to delete from the channel.*"),
                interactions.EmbedField(name="📌 kick [member][reason(Optional)]", value="*↳ The [member] to kick from the server for [reason].*"),
                interactions.EmbedField(name="📌 ban [member][reason(Optional)]", value="*↳ The [member] to ban from the server for [reason].*"),
                interactions.EmbedField(name="📌 unban [member_id]", value="*↳ The [member_id] to unban from the server for [reason].*")
            ]
            embed=createEmbed(title="Aurora Help Message : Moderation", color=1752220, footer_text="The aurora borealis play a part in Chinese dragon legends",
                footer_icon_url = "https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
                thumbnail_url="https://cdn.discordapp.com/attachments/831369746855362590/955340786948505600/unknown.png",
                description="Help Regarding The `Moderation` Category.",
                fields=fields
            )
            await ctx.send(embeds=embed)

def setup(client):
    AuroraHelp(client)
