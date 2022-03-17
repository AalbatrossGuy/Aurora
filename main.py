import interactions, os

client  = interactions.Client(token='TOKEN')


@client.command(
    name="hello",
    description="This is a Hello Command.",
    scope=903225083072495646,
)
async def hello(ctx: interactions.CommandContext):
    await ctx.send("First Command.")

# def load_extension(extension):
#     client.load(f'{extension}.cog')


for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load(f"Cogs.{filename[:-3]}")

client.start()
