from discord.ext import commands


class OnReady(commands.Cog):
    def __int__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot Ready.')


async def setup(client):
    await client.add_cog(OnReady(client))
