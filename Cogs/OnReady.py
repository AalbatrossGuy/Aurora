import interactions

class OnReady(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @command(name="cog", description="This is running from a cog", guild_ids=[903225083072495646])
    async def cog_slash_command(ctx):
        await ctx.send("Sent from a cog!")


def setup(client):
    OnReady(client)
