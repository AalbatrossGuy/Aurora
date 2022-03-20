import interactions, os, json, logging
from datetime import datetime

# CORE SETTINGS
file = open('config.json')
config = json.loads(file.read())
TOKEN = config['Aurora']['TOKEN']
client  = interactions.Client(token=TOKEN)

# LOG SETTINGS
logger = logging.getLogger("auroralog")
logger.setLevel(logging.INFO)
LOG_FILE = 'logs/info.log'
fileHandler = logging.FileHandler(LOG_FILE)
fileHandler.setLevel(logging.INFO)
LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
fileHandler.setFormatter(LOG_FORMAT)
logger.addHandler(fileHandler)

error_logger = logging.getLogger("error-logger")
error_logger.setLevel(logging.DEBUG)
ERROR_LOG_FILE = '././logs/errors.log'
fileErrorHandler = logging.FileHandler(ERROR_LOG_FILE)
fileErrorHandler.setLevel(logging.DEBUG)
ERROR_LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
fileErrorHandler.setFormatter(ERROR_LOG_FORMAT)
error_logger.addHandler(fileErrorHandler)


# COMMANDS
@client.command(
    name="ping",
    description="Shows the bot's latency.",
    scope=903225083072495646,
)
async def _bot_latency(ctx):
    x = len(await client._http.get_application_commands(client.me.id, 903225083072495646))
    print(x)
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


# LOAD COGS
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        try:
            client.load(f"Cogs.{filename[:-3]}")
            logger.info(f"Loaded cogs.{filename[:-3]}")
        except:
            error_logger.error("Error occured while loading Cogs :-", exc_info=True)

logger.info(f"Bot Logged in Discord at - {datetime.now().strftime('%H:%M:%S')}")
client.start()
