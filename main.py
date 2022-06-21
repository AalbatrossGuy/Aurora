import discord, logging, json
from discord import app_commands
from time import perf_counter

file = open("config.json", "r")
config = json.loads(file.read())
TEST_GUILD = discord.Object(id=config["Aurora"]["TEST_GUILD"])
handler = logging.FileHandler(filename="logs/aurora.log", encoding="utf-8", mode="w")


class AuroraClient(discord.AutoShardedClient):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)


client = AuroraClient(intents=discord.Intents.default())


# @client.tree.command(name="add", description="Adds two numbers.")
# @app_commands.rename(first_number="first", second_number="second")
# @app_commands.describe(
#     first_number="The first number",
#     second_number="The second number",
# )
# async def add(interaction: discord.Interaction, first_number: int, second_number: discord.Member):
#     await interaction.response.send_message(f"{first_number} {second_number.id}")

@client.tree.command(name="ping", description="Shows the websocket latency and database latency.")
async def show_latency(interaction: discord.Interaction):
    # ws ping
    embed = discord.Embed(title=":ping_pong: Aurora's Latency", color=discord.Colour.dark_gold(), timestamp=interaction.created_at)
    embed.add_field(name=":green_heart: WS Ping", value=f"```py\n{round(client.latency * 1000)} ms```")
    embed.set_footer(text="Delta Δ is the fourth letter of the Greek Alphabet", icon_url=interaction.user.display_avatar)
    embed.set_thumbnail(url="https://64.media.tumblr.com/be43242341a7be9d50bb2ff8965abf61/tumblr_o1ximcnp1I1qf84u9o1_1280.gif")
    await interaction.response.send_message(embed=embed)

client.run(config["Aurora"]["TOKEN"], log_handler=handler, log_level=logging.INFO)
