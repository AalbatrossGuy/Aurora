import interactions, os

client  = interactions.Client(token='TOKEN')


# def load_extension(extension):
#     client.load(f'{extension}.cog')

@client.command(
    name="ping",
    description="Shows the bot's latency.",
    scope=903225083072495646,
)
async def _bot_latency(ctx):
    connection_latency = client.latency
    websocket_latency = interactions.WebSocketClient.latency
    # print(websocket_latency)
    #await ctx.send(f"{connection_latency.__format__('.2f')} ms")
    embed = interactions.Embed(
        title = "Aurora's Latency",
        color=15158332,
        footer=interactions.EmbedFooter(
            text="The WS Latency & Connection Latency for Aurora.",
            icon_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
        ),
        # thumbnail=interactions.EmbedImageStruct(
        #     url="https://c.tenor.com/2bvE7aaOf6wAAAAC/discord-ping.gif",
        #     height=300,
        #     width=250,
        # ),
        author=interactions.EmbedAuthor(
            name="AalbatrossGuy#5129",
            icon_url="https://media.discordapp.net/attachments/831369746855362590/898903606319800340/IMG_20211009_172918_418.jpg",
        ),
        fields=[
            interactions.EmbedField(
                name="Connection Latency",
                value=f"{connection_latency.__format__('.2f')} ms",
            ),
        ],
    )
    await ctx.send(embeds=embed)



for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load(f"Cogs.{filename[:-3]}")

client.start()
