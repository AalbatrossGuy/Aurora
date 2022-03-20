import interactions, os, json, logging

# CORE SETTINGS
file = open('config.json')
config = json.loads(file.read())
TOKEN = config['Aurora']['TOKEN']
client  = interactions.Client(token=TOKEN)
LOG_FILE = 'logs/info.log'
logging.basicConfig(filename=LOG_FILE, filemode='w', level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
logging.info('Bot Logged in Discord at - {time}')
@client.command(
    name="ping",
    description="Shows the bot's latency.",
    scope=903225083072495646,
)
async def _bot_latency(ctx):
    connection_latency = client.latency
    embed = interactions.Embed(
        title = "Aurora's Latency",
        description=f"{connection_latency.__format__('.2f')} ms",
        color=15158332,
        footer=interactions.EmbedFooter(
            text="The WS Latency & Connection Latency for Aurora.",
            icon_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
        ),
        thumbnail=interactions.EmbedImageStruct(
            url="https://c.tenor.com/2bvE7aaOf6wAAAAC/discord-ping.gif",
            #height=300,
            #width=250,
        )._json,
        author=interactions.EmbedAuthor(
            name="AalbatrossGuy#5129",
            icon_url="https://media.discordapp.net/attachments/831369746855362590/898903606319800340/IMG_20211009_172918_418.jpg",
        ),
    )
    await ctx.send(embeds=embed)


for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load(f"Cogs.{filename[:-3]}")

client.start()
