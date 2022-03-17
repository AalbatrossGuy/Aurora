import interactions

client  = interactions.Client(token='OTUzODI4MjIyODkyNjcwOTg3.YjKPwQ._kVSDVyCOGhnaPJ8lGC9XGINeFE')


@client.command(
    name="hello",
    description="This is a Hello Command.",
    scope=903225083072495646,
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("First Command.", ephemeral=False)

client.start()
