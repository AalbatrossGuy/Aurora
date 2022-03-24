import interactions, json
from customs.customs import createEmbed

class Settings(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.extension_command(
        name="about",
        description="Shows information about the bot.",
        scope=903225083072495646,
    )
    async def _bot_information(self, ctx):
        bot = interactions.User(**await self.client._http.get_self())._json
        client = interactions.User(**await self.client._http.get_self())
        name = bot['username'] + '#' + bot['discriminator']
        # avatar = client.avatar_url
        bio = bot['bio']
        id = bot['id']
        mfa_enabled = bot['mfa_enabled']
        with open('config.json') as file:
            file = json.load(file)
            version = file['Aurora']['VERSION']
            github = file['METADATA']['GITHUB_REPOSITORY']
            license = file['METADATA']['LICENSE']
            devs = "\n".join([file['Aurora']['DEVELOPERS'][0]['DISCORD'], file['Aurora']['DEVELOPERS'][1]['DISCORD']])

        # Embed

        fields = [
            interactions.EmbedField(name="Name", value=name, inline=True),
            interactions.EmbedField(name="ID", value=id, inline=True),
            interactions.EmbedField(name="Version", value=version, inline=True),
            interactions.EmbedField(name="License", value=license, inline=True),
            interactions.EmbedField(name="About Me", value=bio, inline=True),
            interactions.EmbedField(name="mfa_enabled", value=mfa_enabled, inline=True),
            interactions.EmbedField(name="Developers", value=devs, inline=True)
        ]

        embed = createEmbed(title="About AuroraBot", color=15844367, footer_text="A Norwegian scientist was the first to explain the aurora phenomenon.",
            footer_icon_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
            thumbnail_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
            fields=fields
        )

        await ctx.send(embeds=embed)

def setup(client):
    Settings(client)
