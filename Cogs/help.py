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
                name="command_name",
                description="The command whose help message you want to see.",
                type=interactions.OptionType.STRING,
                required=False,
            ),
        ],
    )
    async def help_message(self, ctx: interactions.CommandContext, command_name: str = None):
        if not command_name:
            embed = createEmbed(title='AuroraBot Help Message', color=1752220, footer_text="The oldest known record of an aurora date back to 2600 BC",
            footer_icon_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
            thumbnail_url="https://cdn.icon-icons.com/icons2/2770/PNG/512/chat_message_icon_176706.png",
            description=f"**Total Commands: `{len(await self.client._http.get_application_commands(self.client.me.id, 903225083072495646))}`**\n[Developer #1](https://github.com/AaalbatrossGuy) | [Developer #2](https://github.com/Catto-YFCN) | [Source Code](https://www.youtube.com/watch?v=1vrEljMfXYo)",
            author_name="AalbatrossGuy#5129", author_icon_url="https://media.discordapp.net/attachments/831369746855362590/898903606319800340/IMG_20211009_172918_418.jpg")
            await ctx.send(embeds=embed)


def setup(client):
    AuroraHelp(client)
